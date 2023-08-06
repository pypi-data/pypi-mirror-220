import ast
from typing import Optional

from flake8_numba.rule import Error, Rule
from flake8_numba.utils import (
    get_decorator_location,
    get_decorator_n_args,
    get_pos_arg_from_decorator,
    is_decorated_with,
)


class NBA001(Rule):
    """Inconsistencies in first positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        msg = (
            "NBA001: Signatures provided in first positional argument is not "
            "consistent."
        )

        if is_decorated_with("guvectorize", node):
            decorator_signatures, location = get_pos_arg_from_decorator(0, node)
            if not isinstance(decorator_signatures, list) or not isinstance(
                decorator_signatures[0], tuple
            ):
                return None

            first_length = len(decorator_signatures[0])
            # Different lengths
            if not all(len(t) == first_length for t in decorator_signatures):
                return Error(location.line, location.column, msg)
            return None

        if is_decorated_with("vectorize", node):
            decorator_signatures, location = get_pos_arg_from_decorator(0, node)
            if not isinstance(decorator_signatures, list):
                return None

            signature_sizes = set()
            for signature in decorator_signatures:
                if hasattr(signature, "args"):
                    signature_sizes.add(len(signature.args))

            if len(signature_sizes) != 1:
                return Error(location.line, location.column, msg)

        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA007}


class NBA005(Rule):
    """Mismatch between first positional arg and function signature."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        msg = (
            "NBA005: First positional argument signatures are not matching "
            "function signature."
        )
        args_func_signature = len(node.args.args)

        if is_decorated_with("guvectorize", node):
            decorator_signatures, location = get_pos_arg_from_decorator(0, node)
            if not isinstance(decorator_signatures, list) or not isinstance(
                decorator_signatures[0], tuple
            ):
                return None

            first_length = len(decorator_signatures[0])
            if first_length != args_func_signature:
                return Error(location.line, location.column, msg)
            return None

        if is_decorated_with("vectorize", node):
            decorator_signatures, location = get_pos_arg_from_decorator(0, node)
            if not isinstance(decorator_signatures, list):
                return None

            # Length assumed to be the same as it depends on NBA001
            signature = decorator_signatures[0]
            if hasattr(signature, "args"):
                if len(signature.args) != args_func_signature:
                    return Error(location.line, location.column, msg)

        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA001, NBA007}


class NBA006(Rule):
    """Do not use decorator for bound methods."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with(["guvectorize", "vectorize"], node):
            return None

        parameters = node.args.args
        if parameters:
            first_parameter = parameters[0]
            first_variable_name = first_parameter.arg
            if first_variable_name in ("cls", "self"):
                msg = "NBA006: Cannot use this decorator in bound methods."
                location = get_decorator_location(["vectorize", "guvectorize"], node)
                return Error(location.line, location.column, msg)  # type: ignore

        return None


class NBA007(Rule):
    """Expected X type for first positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with(["guvectorize", "vectorize"], node):
            return None

        if get_decorator_n_args(node, "args") == 0:
            return None

        first_arg, location = get_pos_arg_from_decorator(0, node)
        if is_decorated_with("guvectorize", node):
            msg = (
                "NBA007: Expected a list of tuples for first positional argument. Each"
                " one containing a valid signature of the type `(*input_types, *rtypes)`."
            )
            if not isinstance(first_arg, list):
                return Error(location.line, location.column, msg)
            for signature in first_arg:
                if not isinstance(signature, tuple):
                    return Error(location.line, location.column, msg)
            return None
        if is_decorated_with("vectorize", node):
            msg = (
                "NBA007: Expected a list with each element being `rtype(*input_types)` "
                "with numba types."
            )
            if not isinstance(first_arg, list):
                return Error(location.line, location.column, msg)
            for signature in first_arg:
                if not hasattr(signature, "return_type") or not hasattr(
                    signature, "args"
                ):
                    return Error(location.line, location.column, msg)
            return None
        return None
