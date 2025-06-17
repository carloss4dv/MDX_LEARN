from typing import TypeAlias

from pydantic import ValidationError
from typing_extensions import TypeIs

from ._cube_query_filter_condition import CubeQueryFilterCondition
from ._gaq_filter_condition import GaqFilterCondition, _GaqFilterLeafCondition
from ._operation import RelationalCondition, disjunctive_normal_form_from_condition
from ._pydantic import get_type_adapter

SupportedTarget: TypeAlias = int | float | str


def is_gaq_filter_condition(
    condition: CubeQueryFilterCondition,
    /,
) -> TypeIs[GaqFilterCondition]:
    try:
        gaq_filter_like_condition = get_type_adapter(  # type: ignore[var-annotated]
            GaqFilterCondition  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
        ).validate_python(condition)
    except ValidationError:
        return False

    dnf: tuple[tuple[_GaqFilterLeafCondition, ...]] = (
        disjunctive_normal_form_from_condition(gaq_filter_like_condition)
    )
    (conjunct_conditions,) = dnf
    return all(
        isinstance(leaf_condition.target, SupportedTarget)
        if isinstance(leaf_condition, RelationalCondition)
        else all(
            isinstance(element, SupportedTarget) for element in leaf_condition.elements
        )
        for leaf_condition in conjunct_conditions
    )
