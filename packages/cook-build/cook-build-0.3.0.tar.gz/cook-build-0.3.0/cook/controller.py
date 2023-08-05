import hashlib
import logging
import networkx as nx
from pathlib import Path
from queue import Empty, Queue
from sqlite3 import Connection
import sys
import threading
import time
from typing import Dict, List, Optional, Sequence, Set, Tuple, TYPE_CHECKING, Union
from . import util

if TYPE_CHECKING:
    from .task import Task


LOGGER = logging.getLogger(__name__)
QUERIES = {
    "schema": """
    CREATE TABLE IF NOT EXISTS "tasks" (
        "name" TEXT PRIMARY KEY,
        "digest" TEXT NOT NULL
    )
    """,
    "select": """
        SELECT "digest" FROM "files" WHERE "name" = :name
    """,
    "upsert": """
        INSERT INTO "tasks" ("name", "digest") VALUES (:name, :digest)
        ON CONFLICT("name") DO UPDATE SET "digest" = :digest
    """
}


class Controller:
    """
    Controller to manage dependencies and execute tasks.
    """
    def __init__(self, dependencies: nx.DiGraph, connection: Connection) -> None:
        self.dependencies = dependencies
        self.connection = connection
        self._digest_cache: Dict[Path, Tuple[float, bytes]] = {}

    def resolve_stale_tasks(self, tasks: Optional[List["Task"]] = None) -> Set["Task"]:
        self.is_stale(tasks or list(self.dependencies))
        return {node for node, data in self.dependencies.nodes(True) if data.get("is_stale")}

    def _evaluate_path_digest(self, path: Path) -> bytes:
        """
        Evaluate the digest of a file.
        """
        path = Path(path).resolve()
        cached = self._digest_cache.get(path)
        if cached:
            digested, digest = cached
            if path.stat().st_mtime < digested:
                return digest
        digest = util.evaluate_digest(path)
        self._digest_cache[path] = (time.time(), digest)
        return digest

    def _evaluate_task_hexdigest(self, task: "Task") -> bytes:
        """
        Evaluate the digest of a task by combining the digest of all its dependencies.
        """
        dependencies = []
        for dependency in task.dependencies:
            dependency = Path(dependency).resolve()
            if not dependency.is_file():
                LOGGER.debug("dependency %s of %s is missing", dependency, task)
                return None
            dependencies.append(dependency)

        hasher = hashlib.sha1()
        for dependency in sorted(dependencies):
            hasher.update(util.evaluate_digest(dependency))
        return hasher.hexdigest()

    def is_stale(self, task: Union["Task", Sequence["Task"]]) -> Union[bool, List[bool]]:
        """
        Determine if one or more tasks are stale.

        Args:
            task: Task or tasks to check.

        Returns:
            If the task or tasks are stale.
        """
        if isinstance(task, Sequence):
            return [self.is_stale(x) for x in task]

        is_stale = self.dependencies.nodes[task].get("is_stale")
        if is_stale is not None:
            return is_stale
        is_stale = self._is_self_stale(task)
        successors = list(self.dependencies.successors(task))
        if successors:
            is_stale |= any(self.is_stale(successors))
        self.dependencies.nodes[task]["is_stale"] = is_stale
        return is_stale

    def _is_self_stale(self, task: "Task") -> bool:
        """
        Determine whether a task is *itself* stale irrespective of other tasks it may depend on.

        Args:
            task: Task to check.

        Returns:
            If the task is stale, ignoring dependencies.
        """
        # If there are no targets or the targets are missing, the task is stale.
        if not task.targets:
            LOGGER.debug('%s is stale because it has no targets', task)
            return True
        for target in task.targets:
            if not target.is_file():
                LOGGER.debug("%s is stale because its target `%s` is missing", task, target)
                return True

        # If there is no digest in the database, the task is stale.
        cached_digest = self.connection.execute("SELECT digest FROM tasks WHERE name = :name",
                                                {"name": task.name}).fetchone()
        if cached_digest is None:
            LOGGER.debug("%s is stale because it does not have a hash entry", task)
            return True

        # If one of the dependencies is missing, the task is stale.
        current_digest = self._evaluate_task_hexdigest(task)
        if current_digest is None:
            LOGGER.debug("%s is stale because one of its dependencies is missing", task)

        # If the digest has changed, the task is stale.
        cached_digest, = cached_digest
        if current_digest != cached_digest:
            LOGGER.debug("%s is stale because one of its dependencies has changed (cached digest: "
                         "%s, current digest: %s)", task, cached_digest, current_digest)
            return True

        LOGGER.debug("%s is up to date", task)
        return False

    def execute(self, tasks: "Task", num_concurrent: int = 1, interval: float = 1) -> None:
        """
        Execute one or more tasks.

        Args:
            tasks: Tasks to execute.
            num_concurrent: Number of concurrent threads to run.
        """
        if not isinstance(tasks, Sequence):
            tasks = [tasks]
        if not any(self.is_stale(tasks)):
            return

        # Start the worker threads.
        threads: List[threading.Thread] = []
        input_queue = Queue()
        output_queue = Queue()
        stop = util.StopEvent(interval)
        for i in range(num_concurrent):
            thread = threading.Thread(target=self._target, name=f"cook-thread-{i}",
                                      args=(stop, input_queue, output_queue), daemon=True)
            thread.start()
            threads.append(thread)

        # Create a copy of the dependency graph and filter it to remove all non-stale tasks.
        dependencies: nx.DiGraph = self.dependencies.copy()
        not_stale = [node for node, data in dependencies.nodes.data() if not data.get("is_stale")]
        dependencies.remove_nodes_from(not_stale)

        # Initialize the input queue with leaf nodes.
        for node, out_degree in dependencies.out_degree():
            if out_degree == 0:
                input_queue.put(node)

        try:
            while dependencies.number_of_nodes():
                # Try to get the next item in the queue, continuing if there's nothing available.
                try:
                    item: Optional[Tuple["Task", sys._OptExcInfo]] = \
                        output_queue.get(timeout=interval)
                except Empty:
                    continue

                # Check if the stop event is set and abort if so.
                if stop.is_set():
                    break

                assert item is not None, "output queue returned `None`; this is a bug"

                # Unpack the results.
                task, exc_info = item
                if exc_info:
                    raise util.FailedTaskError(task=task) from exc_info[1]

                # Add tasks that are now leaf nodes to the tree.
                predecessors = list(dependencies.predecessors(task))
                dependencies.remove_node(task)
                self.dependencies.add_node(task, is_stale=False)
                for node, out_degree in dependencies.out_degree(predecessors):
                    if out_degree == 0:
                        input_queue.put(node)

                # Verify that targets were created.
                for target in task.targets:
                    if not target.is_file():
                        raise util.FailedTaskError(f"`{task}` did not create `{target}`",
                                                   task=task)
                    LOGGER.debug("%s created `%s`", task, target)

                # Update the status in the database.
                params = {"name": task.name, "digest": self._evaluate_task_hexdigest(task)}
                self.connection.execute(QUERIES["upsert"], params)
                self.connection.commit()
        finally:
            # Set the stop event and add "None" to the queue so the workers stop waiting.
            LOGGER.debug("set stop event for threads: %s", [thread.name for thread in threads])
            stop.set()
            for thread in threads:
                input_queue.put(None)

            # Shut down the worker threads.
            for thread in threads:
                thread.join(stop.interval)
                if thread.is_alive():  # pragma: no cover
                    raise RuntimeError(f"thread {thread} failed to join")

    def _target(self, stop: util.StopEvent, input_queue: Queue, output_queue: Queue) -> None:
        LOGGER.debug(f"started thread `{threading.current_thread().name}`")
        while not stop.is_set():
            try:
                task: "Task" = input_queue.get(stop.interval)
            except Empty:  # pragma: no cover
                # It's unlikely there's nothing on the queue, but let's handle it anyway.
                continue
            # Check the stop event before executing the task; it may have been set while we were
            # waiting for the next task in the queue.
            if stop.is_set():
                break

            assert task is not None, "input queue returned `None`; this is a bug"

            try:
                LOGGER.info("executing %s ...", task)
                task.execute(stop)
                output_queue.put((task, None))
                LOGGER.info("completed %s", task)
            except:  # noqa: E722
                exc_info = sys.exc_info()
                LOGGER.exception("failed to execute %s", task, exc_info=exc_info)
                output_queue.put((task, sys.exc_info()))

        # Put anything on the queue in case the parent is waiting.
        LOGGER.debug(f"exiting thread `{threading.current_thread().name}`")
        output_queue.put(None)

    def reset(self, *tasks: "Task") -> None:
        params = [{"name": task.name for task in tasks}]
        self.connection.executemany("DELETE FROM tasks WHERE name = :name", params)
        self.connection.commit()
        LOGGER.info("reset %d %s", len(tasks), "task" if len(tasks) == 1 else "tasks")
