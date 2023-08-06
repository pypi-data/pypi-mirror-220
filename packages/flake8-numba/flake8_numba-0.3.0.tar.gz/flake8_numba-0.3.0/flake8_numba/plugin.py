"""Module that implement the main `Plugin` logic class."""
import ast
import importlib.metadata as importlib_metadata
from collections.abc import Generator
from typing import Any

from flake8_numba.visitor import Visitor


class Plugin:
    """Class used by Flake8 to find specific issues."""

    name = __name__.split(".", 1)[0]
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST):
        """Instantiet the class with the tree object passed by Flake8."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Run and iterate over the tree object to find issues."""
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
