import ast
import re
from collections import Counter
from typing import Any, Optional, cast

from flake8_numba.rule import Error, Rule
from flake8_numba.rules import nba0
from flake8_numba.utils import (
    Location,
    get_decorator_location,
    get_decorator_n_args,
    get_numba_signature_info,
    get_pos_arg_from_decorator,
    has_return_value,
    is_decorated_with,
)


class NBA201(Rule):
    """Non matching number of inputs/outputs between both positional arguments."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        first = get_pos_arg_from_decorator(0, node)
        second = get_pos_arg_from_decorator(1, node)
        if not isinstance(second.numba_signature, str) or not isinstance(
            first.numba_signature, list
        ):
            return None
        len_second_arg = Counter(second.numba_signature)["("]

        for idx, signature in enumerate(first.numba_signature):
            n_args = get_numba_signature_info(signature, mode="n_args")
            if n_args != len_second_arg:
                msg = (
                    f"NBA201: Number of inputs/outputs in first signature ({idx}) is not "
                    "matching the one provided in the second argument."
                )
                return Error(first.location.line, first.location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007, NBA203, NBA204}  # First two positional arguments are ok


class NBA202(Rule):
    """Non matching sizes of inputs/outputs between both positional arguments."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        first = get_pos_arg_from_decorator(0, node)
        first_arg = cast(list[tuple[Any, ...]], first.numba_signature)
        second = get_pos_arg_from_decorator(1, node)

        # Get sizes from second positional argument
        pattern = r"\(((?:[a-zA-Z]+(?:,\s*[a-zA-Z]+)*)?)\)"
        sizes_from_second_arg: list[int] = []
        symbol: str
        if second.numba_signature is None or not isinstance(second.numba_signature, str):
            return None
        for match in re.findall(pattern, second.numba_signature):
            count = 0
            for symbol in match:
                if symbol.isalpha():
                    count += 1
            sizes_from_second_arg.append(count)

        sizes_from_first_arg: list[int] = []
        for signature in first_arg:
            sizes_from_first_arg = []
            for value in get_numba_signature_info(signature, mode="args"):
                if hasattr(value, "ndim"):
                    sizes_from_first_arg.append(value.ndim)
                else:
                    sizes_from_first_arg.append(0)
            if sizes_from_first_arg != sizes_from_second_arg:
                msg = (
                    f"NBA202: Sizes between first signature ({sizes_from_first_arg}) "
                    f"and second positional argument ({sizes_from_second_arg}) are "
                    "not matching."
                )
                return Error(second.location.line, second.location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA201}  # First two positional arguments are ok


class NBA203(Rule):
    """Undefined symbol in second positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        second = get_pos_arg_from_decorator(1, node)
        signature = second.numba_signature
        if not isinstance(signature, str):
            return None
        count = Counter(signature)
        if "->" not in signature or count[")"] < 2 or count["("] < 2 or count["-"] > 1:
            return None

        inputs, outputs = signature.split("->")
        diff = set(outputs) - set(inputs)
        for elem in diff:
            if elem.isalpha():
                msg = f"NBA203: Symbol `{elem}` must be also defined on the left side."
                return Error(second.location.line, second.location.column, msg)

        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA206, NBA207, NBA208}  # 2 args, no open parenthesis + second pos is str


class NBA204(Rule):
    """Constants are not allowed in second positional argument."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        signature, _, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return None
        count = Counter(signature)
        if "->" not in signature or count[")"] < 2 or count["("] < 2 or count["-"] > 1:
            return None

        for elem in signature:
            if elem.isdigit():
                msg = (
                    f"NBA204: Constants (`{elem}`) are not allowed in the second "
                    "signature."
                )
                return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA206, NBA207, NBA208}  # 2 args, no open parenthesis + second pos is str


class NBA205(Rule):
    """Guvectorize function shall return None."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        has_return, location = has_return_value(node)
        if has_return and is_decorated_with("guvectorize", node):
            msg = (
                "NBA205: Functions decorator with `@guvectorize` cannot return any value."
            )
            return Error(location.line, location.column, msg)
        return None


class NBA206(Rule):
    """Open parenthesis in second position argument signature."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if not is_decorated_with("guvectorize", node):
            return None
        if get_decorator_n_args(node, "args") != 2:
            return None
        signature, _, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(signature, str):
            return None
        counter = Counter(signature)
        if counter["("] != counter[")"]:
            msg = "NBA206: Parenthesis on second positional argument are broken."
            return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007}


class NBA207(Rule):
    """Second argument must define the sizes-related signature (string type)."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if (
            not is_decorated_with("guvectorize", node)
            or get_decorator_n_args(node, "args") != 2
        ):
            return None
        signature, _, location = get_pos_arg_from_decorator(1, node)
        if signature is None:
            return None

        msg = (
            "NBA207: A second signature (str type) must be provided with "
            "corresponding sizes of inputs and outputs."
        )
        if not isinstance(signature, str):  # If numba based signature
            return Error(location.line, location.column, msg)
        counter = Counter(signature)
        if counter["("] < 2 or counter[")"] < 2 or "->" not in signature:
            return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA208, nba0.NBA007}


class NBA208(Rule):
    """Guvectorize needs two positional arguments."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        if is_decorated_with("guvectorize", node):
            first_arg = get_pos_arg_from_decorator(0, node)
            second_arg = get_pos_arg_from_decorator(1, node)

            msg = (
                "NBA208: Guvectorize strictly needs two positional arguments: string/list"
                " for the first one and string for the second."
            )
            location = get_decorator_location("guvectorize", node)
            location = cast(Location, location)
            if get_decorator_n_args(node, "args") != 2:
                return Error(location.line, location.column, msg)
            if isinstance(first_arg[0], list):
                if len(first_arg[0]) == 0:
                    return Error(location.line, location.column, msg)
            if not isinstance(second_arg.ast_expr, ast.Str):
                return Error(location.line, location.column, msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007}


class NBA209(Rule):
    """Output value is not assigned with guvectorize."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        str_signature, _, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(str_signature, str):
            return None

        parts = str_signature.split("->")
        right_of_arrow = parts[1].strip()
        n_outputs = Counter(right_of_arrow)["("]

        # Get the function body
        func_body = node.body

        # Get the names of the last N positional arguments of the function
        outputs_to_be_modified = {
            arg.arg for arg in node.args.args[-n_outputs:] if arg.annotation is None
        }

        # Traverse each node in the function body
        for sub_node in func_body:
            # If it is an assignment and the target is a name argument
            if isinstance(sub_node, ast.Assign) and isinstance(
                sub_node.targets[0], ast.Subscript
            ):
                value = sub_node.targets[0].value
                if isinstance(value, ast.Name) and value.id in outputs_to_be_modified:
                    outputs_to_be_modified.remove(value.id)

        if outputs_to_be_modified:
            msg = (
                "NBA209: Not all output variables are assigned: "
                f"{','.join(list(outputs_to_be_modified))}"
            )
            return Error(location.line, location.column, message=msg)
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {NBA201, NBA202, NBA203, NBA204, NBA205, nba0.NBA005}


class NBA211(Rule):
    """Arrays in second pos argument must be separated by commas."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        second_arg, _, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(second_arg, str):
            return None

        closing_detected = False
        arrow_detected = False
        comma_detected = False
        for char in second_arg:
            if char == ")":
                closing_detected = True
            elif char == ",":
                comma_detected = True
            elif char == "-":
                arrow_detected = True
            elif char == "(":
                if closing_detected and not comma_detected and not arrow_detected:
                    msg = (
                        "NBA211: Arrays on second positional argument must be separated "
                        "by commas."
                    )
                    return Error(location.line, location.column, msg)
                closing_detected = False
                comma_detected = False
                arrow_detected = False
        return None

    @property
    def depends_on(self) -> set[type[Rule]]:
        return {nba0.NBA007, NBA203, NBA204}  # First two positional arguments are ok


class NBA212(Rule):
    """Do not assign en input variables."""

    def _check(self, node: ast.FunctionDef) -> Optional[Error]:
        str_signature, _, location = get_pos_arg_from_decorator(1, node)
        if not isinstance(str_signature, str):
            return None

        parts = str_signature.split("->")
        right_of_arrow = parts[0].strip()
        n_inputs = Counter(right_of_arrow)["("]

        # Get the function body
        func_body = node.body

        # Get the names of the first N positional arguments of the function
        input_names = {
            arg.arg for arg in node.args.args[:n_inputs] if arg.annotation is None
        }

        # Traverse each node in the function body
        for sub_node in func_body:
            # If it is an assignment and the target is a name argument
            if isinstance(sub_node, ast.Assign):
                targets = sub_node.targets
                if isinstance(targets[0], ast.Name) and targets[0].id in input_names:
                    msg = f"NBA212: Do not modify input value: {targets[0].id}"
                    return Error(location.line, location.column, message=msg)
                if isinstance(targets[0], ast.Subscript) and isinstance(
                    targets[0].value, ast.Name
                ):
                    if targets[0].value.id in input_names:
                        msg = f"NBA212: Do not modify input value: {targets[0].value.id}"
                        return Error(location.line, location.column, message=msg)
        return None
