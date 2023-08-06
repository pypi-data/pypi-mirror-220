import argparse
import colorama
import fnmatch
import importlib.util
import logging
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Iterable, List, Optional
from .contexts import create_target_directories, normalize_action, normalize_dependencies
from .controller import Controller, QUERIES
from .manager import Manager
from .task import Task
from .util import FailedTaskError


LOGGER = logging.getLogger("cook")


class NoMatchingTaskError(ValueError):
    def __init__(self, patterns: Iterable[re.Pattern]):
        patterns = [f"`{pattern}`" for pattern in patterns]
        if len(patterns) == 1:
            message = f"found no tasks matching pattern {patterns[0]}"
        else:
            *patterns, last = patterns
            message = "found no tasks matching patterns " + ", ".join(patterns) \
                + (", or " if len(patterns) > 1 else " or ") + last
        super().__init__(message)


def discover_tasks(tasks: Iterable[Task], patterns: Iterable[re.Pattern], use_re: bool) \
        -> List[Task]:
    """
    Discover tasks based on regular expressions.
    """
    if not patterns:
        return list(tasks)
    tasks = [task for task in tasks if any(
        re.match(pat, task.name) if use_re else fnmatch.fnmatch(task.name, pat) for pat in patterns
    )]
    if not tasks:
        raise NoMatchingTaskError(patterns)
    return tasks


class Command:
    """
    Abstract base class for commands.
    """
    NAME: Optional[str] = None

    def __init__(self) -> None:
        pass

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        raise NotImplementedError

    def execute(self, controller: Controller, args: argparse.Namespace) -> None:
        raise NotImplementedError


class ExecArgs(argparse.Namespace):
    tasks: Iterable[re.Pattern]
    re: bool
    jobs: int


class ExecCommand(Command):
    """
    Execute one or more tasks.
    """
    NAME = "exec"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--re", "-r", action="store_true",
                            help="use regular expressions for pattern matching instead of glob")
        parser.add_argument("--jobs", "-j", help="number of concurrent jobs", type=int, default=1)
        parser.add_argument("tasks", nargs="+",
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: ExecArgs) -> None:
        tasks = discover_tasks(controller.dependencies, args.tasks, args.re)
        controller.execute(tasks, num_concurrent=args.jobs)


class LsArgs(argparse.Namespace):
    tasks: Iterable[re.Pattern]
    all: bool
    re: bool


class LsCommand(Command):
    """
    List tasks.
    """
    NAME = "ls"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--all", "-a", action="store_true",
                            help="include tasks starting with `_` prefix")
        parser.add_argument("--re", "-r", action="store_true",
                            help="use regular expressions for pattern matching instead of glob")
        parser.add_argument("tasks", nargs="*",
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: LsArgs) -> None:
        tasks = discover_tasks(controller.dependencies, args.tasks, args.re)
        if not args.all:
            tasks = [task for task in tasks if not task.name.startswith("_")]
        print("\n".join(map(str, tasks)))


class InfoArgs(argparse.Namespace):
    pass


class InfoCommand(Command):
    """
    Display information about one or more tasks.
    """
    NAME = "info"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("tasks", nargs="*",
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: InfoArgs) -> None:
        print(self)


class ResetArgs(argparse.Namespace):
    tasks: Iterable[re.Pattern]
    re: bool


class ResetCommand(Command):
    """
    Reset the status of one or more tasks.
    """
    NAME = "reset"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--re", "-r", action="store_true",
                            help="use regular expressions for pattern matching instead of glob")
        parser.add_argument("tasks", nargs="*",
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: ResetArgs) -> None:
        controller.reset(*discover_tasks(controller.dependencies, args.tasks, args.re))


class Formatter(logging.Formatter):
    COLOR_BY_LEVEL = {
        "DEBUG": colorama.Fore.MAGENTA,
        "INFO": colorama.Fore.BLUE,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.WHITE + colorama.Back.RED,
    }
    RESET = colorama.Fore.RESET + colorama.Back.RESET

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLOR_BY_LEVEL[record.levelname]
        return f"{color}{record.levelname}{self.RESET}: {record.getMessage()}"


def __main__(cli_args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser("cook")
    parser.add_argument("--recipe", help="file containing declarative recipe for tasks",
                        default="recipe.py", type=Path)
    parser.add_argument("--module", "-m", help="module containing declarative recipe for tasks")
    parser.add_argument("--db", help="database for keeping track of assets", default=".cook")
    parser.add_argument("--log-level", help="log level", default="info",
                        choices={"error", "warning", "info", "debug"})
    subparsers = parser.add_subparsers()
    subparsers.required = True

    for command_cls in [ExecCommand, LsCommand, InfoCommand, ResetCommand]:
        subparser = subparsers.add_parser(command_cls.NAME, help=command_cls.__doc__)
        command = command_cls()
        command.configure_parser(subparser)
        subparser.set_defaults(command=command)

    args = parser.parse_args(cli_args)

    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    logging.basicConfig(level=args.log_level.upper(), handlers=[handler])

    with Manager() as manager:
        try:
            manager.contexts.extend([
                create_target_directories(),
                normalize_action(),
                normalize_dependencies(),
            ])
            if args.module:
                # Temporarily add the current working directory to the path.
                try:
                    sys.path.append(os.getcwd())
                    importlib.import_module(args.module)
                finally:
                    sys.path.pop()
            elif args.recipe.is_file():
                # Parse the recipe.
                spec = importlib.util.spec_from_file_location("recipe", args.recipe)
                recipe = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(recipe)
            else:  # pragma: no cover
                raise ValueError("recipe file or module must be specified; default recipe.py not "
                                 "found")
        except:  # noqa: E722
            LOGGER.fatal("failed to load recipe")
            sys.exit(1)

    with sqlite3.connect(args.db) as connection:
        connection.execute(QUERIES["schema"])
        controller = Controller(manager.resolve_dependencies(), connection)
        command: Command = args.command
        try:
            command.execute(controller, args)
        except KeyboardInterrupt:  # pragma: no cover
            LOGGER.warning("interrupted by user")
        except NoMatchingTaskError as ex:
            LOGGER.warning(ex)
            sys.exit(1)
        except FailedTaskError:
            sys.exit(1)


if __name__ == "__main__":
    __main__()
