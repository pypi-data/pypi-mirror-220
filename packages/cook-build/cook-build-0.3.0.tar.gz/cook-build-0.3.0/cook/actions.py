r"""
Actions
-------

Actions are performed when tasks are executed. Builtin actions include calling python functions
using :class:`.FunctionAction`, running subprocesses using :class:`.SubprocessAction`, and composing
multiple actions using :class:`.CompositeAction`.

Custom actions can be implemented by inheriting from :class:`.Action` and implementing the
:meth:`~.Action.execute` method which receives a :class:`~.task.Task`. The method should execute the
action; its return value is ignored. For example, the following action waits for a specified time.

.. doctest::

    >>> from cook.actions import Action
    >>> from time import sleep, time

    >>> class SleepAction(Action):
    ...     def __init__(self, delay: float) -> None:
    ...         self.delay = delay
    ...
    ...     def execute(self, task: Task) -> None:
    ...         start = time()
    ...         sleep(self.delay)
    ...         print(f"time: {time() - start:.3f}")

    >>> action = SleepAction(0.1)
    >>> action.execute(None)
    time: 0.1...
"""
import subprocess
from typing import Callable, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .task import Task
    from .util import StopEvent


class Action:
    """
    Action to perform when a task is executed in its own thread.
    """
    def execute(self, task: "Task", stop: Optional["StopEvent"] = None) -> None:
        """
        Execute the action.
        """
        raise NotImplementedError


class FunctionAction(Action):
    """
    Action wrapping a python callable.

    Args:
        func: Function to call which must accept a :class:`~.task.Task` as its first argument.
        *args: Additional positional arguments.
        **kwargs: Keyword arguments.
    """
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self, task: "Task", stop: Optional["StopEvent"] = None) -> None:
        self.func(task, *self.args, **self.kwargs)


class SubprocessAction(Action):
    """
    Run a subprocess.

    Args:
        program: Program to run.
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Example:

        .. doctest::

            >>> from cook.actions import SubprocessAction
            >>> from pathlib import Path

            >>> action = SubprocessAction(["touch", "hello.txt"])
            >>> action.execute(None)
            >>> Path("hello.txt").is_file()
            True
    """
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def execute(self, task: "Task", stop: Optional["StopEvent"] = None) -> None:
        # Repeatedly wait for the process to complete, checking the stop event after each poll.
        interval = stop.interval if stop else None
        process = subprocess.Popen(*self.args, **self.kwargs)
        while True:
            try:
                returncode = process.wait(interval)
                if returncode:
                    raise subprocess.CalledProcessError(returncode, process.args)
                return
            except subprocess.TimeoutExpired:
                if stop.is_set():
                    break

        # Clean up the process by trying to terminate it and then killing it.
        for method in [process.terminate, process.kill]:
            method()
            try:
                returncode = process.wait(max(interval, 3))
                if returncode:
                    raise subprocess.CalledProcessError(returncode, process.args)
                # The process managed to exit gracefully after the main loop. This is unlikely.
                return  # pragma: no cover
            except subprocess.TimeoutExpired:  # pragma: no cover
                pass

        # We couldn't kill the process. Also very unlikely.
        raise subprocess.SubprocessError(f"failed to shut down {process}")  # pragma: no cover


class CompositeAction(Action):
    """
    Execute multiple actions in order.

    Args:
        *actions: Actions to execute.
    """
    def __init__(self, *actions: Action) -> None:
        self.actions = actions

    def execute(self, task: "Task", stop: Optional["StopEvent"] = None) -> None:
        for action in self.actions:
            action.execute(task, stop)
