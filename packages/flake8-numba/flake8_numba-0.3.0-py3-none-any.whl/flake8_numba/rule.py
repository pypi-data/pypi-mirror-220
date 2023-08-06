"""Module that implement the logic that all rules will follow."""
import ast
from abc import ABC, abstractmethod
from typing import ClassVar, NamedTuple, Optional, final


class Error(NamedTuple):
    """Class that holds all the information relative to a single error."""

    line: int
    """Line where the error is located."""
    column: int
    """Column where the error is located."""
    message: str
    """Message of the error."""


class Rule(ABC):
    """Skeleton that all rules have to meet."""

    all_rules: ClassVar[list["Rule"]] = []
    """List of all rules implemented so far."""

    @final
    def check(self, node: ast.FunctionDef, errors: list[Error]) -> bool:
        """Check if the current rule is found to be broken within node.

        Returns `True` if no error. `False` if it was ok.

        Args:
            node (ast.FunctionDef): Node describing the function definition.
            errors (list[Error]): Current list of errors founds. If new errors are found,
                they will be added to this list.
        """
        if errors is None:
            errors = []
        error = self._check(node)
        if error:
            errors.append(error)
            return False
        return True

    @abstractmethod
    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        """Given a node, find any possible issues.

        Args:
            node (ast.FunctionDef): Node that represents a small piece code.
        """
        ...

    @property
    def depends_on(self) -> set[type["Rule"]]:
        """Check will be automatically skip if these errors were triggered first.

        Meant to be overridden to add more rules.

        Returns:
             set[type[Rule], ...]: Tuple with all codes.
        """
        return set()

    def __init_subclass__(cls, **kwargs: object):
        """Populate `all_rules` variable with all subclasses."""
        super().__init_subclass__(**kwargs)
        cls.all_rules.append(cls())
