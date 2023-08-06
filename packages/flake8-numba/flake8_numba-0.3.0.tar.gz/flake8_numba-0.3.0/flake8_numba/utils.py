import ast
from collections.abc import Iterable, Mapping, Sequence
from functools import lru_cache
from typing import Literal, NamedTuple, Optional, Union, overload

import numba  # noqa: F401


class Location(NamedTuple):
    """Define the location for a given error."""

    line: int = 0
    column: int = 0


def get_decorator_location(
    decorator_names: Union[Iterable[str], str], node: ast.FunctionDef
) -> Optional[Location]:
    """Get the location of a given decorator(s).

    Args:
        decorator_names (Union[Iterable[str], str]): Decorators to check.
        node (ast.FunctionDef): Node representing the function definition.

    Returns:
        Optional[Location]: Location of the decorator. None if it could not be found for
            the given names.
    """
    decorator_names_ = (
        [decorator_names] if isinstance(decorator_names, str) else decorator_names
    )
    if node.decorator_list:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                name = (
                    decorator.func.attr
                    if isinstance(decorator.func, ast.Attribute)
                    else decorator.func.id  # type: ignore
                )
            else:
                name = (
                    decorator.attr
                    if isinstance(decorator, ast.Attribute)
                    else decorator.id  # type: ignore
                )
            if name in decorator_names_:
                return Location(decorator.lineno, decorator.col_offset)

    return None


def is_decorated_with(
    decorator_names: Union[Iterable[str], str], node: ast.FunctionDef
) -> bool:
    """Check if a function is decorated with the given decorator names.

    Args:
        decorator_names (Union[Iterable[str], str]): Decorators to check.
        node (ast.FunctionDef): Node representing the function definition.

    Returns:
        bool: `True` if any of the decorators could be found.
    """
    decorator_names_ = (
        [decorator_names] if isinstance(decorator_names, str) else decorator_names
    )
    if node.decorator_list:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                name = (
                    decorator.func.attr
                    if isinstance(decorator.func, ast.Attribute)
                    else decorator.func.id  # type: ignore
                )
            else:
                name = (
                    decorator.attr
                    if isinstance(decorator, ast.Attribute)
                    else decorator.id  # type: ignore
                )
            if name in decorator_names_:
                return True

    return False


def has_return_value(func_ast: ast.FunctionDef) -> tuple[bool, Location]:
    """Check if a given function has any return value.

    Args:
        func_ast (ast.FunctionDef): Function to be inspected.

    Returns:
        tuple[bool, Location]: Boolean value indicating whether there is and its
            corresponding location.
    """
    for node in ast.walk(func_ast):
        if isinstance(node, ast.Return) and node.value is not None:
            return True, Location(line=node.lineno, column=node.col_offset)
    return False, Location()


def decorator_has_arguments(node: ast.FunctionDef) -> bool:
    """Check whether a function has a decortor with arguments.

    Args:
        node (ast.FunctionDef): Node representing the function definition.

    Returns:
        bool: `True` if the function is decorated AND it uses arguments. `False`
            otherwise.
    """
    if not node.decorator_list:
        return False

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and decorator.args:
            return True

    return False


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal["args"]) -> int:
    ...


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal["kwargs"]) -> int:
    ...


@overload
def get_decorator_n_args(node: ast.FunctionDef, arg_type: Literal[""] = "") -> int:
    ...


def get_decorator_n_args(node: ast.FunctionDef, arg_type: str = "") -> int:
    """Get number of arguments in decorator.

    Args:
        node (ast.FunctionDef): Node representing the function definition.
        arg_type (Union[Literal["kwargs"],Literal["args"],Literal[""]]): Specify which
            arguments are counted. Positional, kwargs or both. Both by default.

    Returns:
        int: Count of positional arguments for the decorator.
    """
    if not node.decorator_list:
        return 0

    args_count: int = 0
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and decorator.args:
            if arg_type in ("args", ""):
                for arg in decorator.args:
                    if isinstance(arg, ast.AST):
                        args_count += 1
        if isinstance(decorator, ast.Call) and decorator.keywords:
            if arg_type in ("kwargs", ""):
                for keyword in decorator.keywords:
                    if isinstance(keyword, ast.keyword):
                        args_count += 1
    return args_count


@lru_cache
def _dct_custom_alias_to_standard_numba() -> Mapping[str, str]:
    """Get a dictionary that can be used to parse from custom to standard numba types.

    This is useful to detect cases such as `nb.float32` instead of `numba.float32`.

    Returns:
        Mapping[str, str]: Dictionary that links custom data type to "standard" numba
            type.
    """
    _aliases: Sequence[tuple[set[str], str]] = [
        ({"boolean", "bool_", "b1"}, "numba.boolean"),
        ({"uint8", "byte", "u1"}, "numba.uint8"),
        ({"uint16", "u2"}, "numba.uint16"),
        ({"uint32", "u2"}, "numba.uint32"),
        ({"uint64", "u4"}, "numba.uint64"),
        ({"int8", "char", "i1"}, "numba.int8"),
        ({"int16", "i2"}, "numba.int16"),
        ({"int32", "i4"}, "numba.int32"),
        ({"int64", "i8"}, "numba.int64"),
        ({"intc"}, "numba.intc"),
        ({"uintc"}, "numba.uintc"),
        ({"intp"}, "numba.intp"),
        ({"uintp"}, "numba.uintp"),
        ({"float32", "f4"}, "numba.float32"),
        ({"double", "f8", "float64"}, "numba.float64"),
        ({"complex64", "c8"}, "numba.complex64"),
        ({"complex128", "c16"}, "numba.complex128"),
    ]

    possible_prefix = ("nb.", "")

    dct_aliases = {}
    for alias_type in _aliases:
        for alias in alias_type[0]:
            for possible_prefix_ in possible_prefix:
                dct_aliases[alias] = f"{possible_prefix_}{alias_type[1]}"
    return dct_aliases


def get_pos_arg_from_decorator(
    at: int, node: ast.FunctionDef
) -> tuple[Optional[object], Location]:
    """Get the indicated positional argument.

    Args:
        at (int): Index of the positional argument
        node (ast.FunctionDef): Node representing the function definition.

    Returns:
        tuple[Optional[object], Location]: Argument as an `object` if the code could
            be evaluated (including `numba` library), string representation otherwise.
    """
    if not node.decorator_list or not decorator_has_arguments(node):
        return None, Location()

    if at >= get_decorator_n_args(node, "args"):
        return None, Location()

    arg = node.decorator_list[0].args[at]  # type: ignore
    location = Location(line=arg.lineno, column=arg.col_offset)
    original_str = ast.unparse(arg)
    custom_to_standard = _dct_custom_alias_to_standard_numba()
    new_str = original_str
    while True:
        try:
            return eval(new_str), location  # noqa: PGH001
        except NameError as name_error:
            not_found_variable_name = name_error.args[0].split()[1].strip("'")
            if not_found_variable_name == "nb":
                new_str = new_str.replace("nb.", "")
            elif not_found_variable_name in custom_to_standard:
                new_str = new_str.replace(
                    not_found_variable_name, custom_to_standard[not_found_variable_name]
                )
            else:
                return original_str, location
        except Exception:  # noqa: BLE001
            return None, Location()
