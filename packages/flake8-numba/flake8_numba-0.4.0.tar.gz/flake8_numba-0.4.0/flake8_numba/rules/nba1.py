import ast
from typing import Optional

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import is_decorated_with


class NBA101(Rule):
    """Only one value can be returned with `vectorize`."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with("vectorize", node):
            return None

        return_count = 0
        # Check the 'return' statement in the function body
        for statement in node.body:
            if isinstance(statement, ast.Return):
                if isinstance(statement.value, ast.Tuple):
                    return_elements = statement.value.elts
                    return_count = max(return_count, len(return_elements))

        if return_count > 1:
            msg = "NBA101: Only one value can be returned."
            return Error(statement.lineno, statement.col_offset, msg)
        return None


class NBA102(Rule):
    """Expected return value for the function."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with("vectorize", node):
            return None

        # Check the 'return' statement in the function body
        for statement in node.body:
            if isinstance(statement, ast.Return):
                return None

        msg = "NBA102: Functions decorated with `vectorize` must have one return value"
        return Error(statement.lineno, statement.col_offset, msg)
