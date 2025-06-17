from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass

from ._base_cube_definition import BaseCubeDefinition
from ._cube_filter_condition import CubeFilterCondition
from ._identification import (
    ApplicationName,
    CubeCatalogNames,
    Identifiable,
    TableIdentifier,
)
from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class CubeDefinition(BaseCubeDefinition):
    fact_table: Identifiable[TableIdentifier]

    _: KW_ONLY

    """The definition to create a :class:`~atoti.Cube`."""

    application_name: ApplicationName | None = None
    """The name of the application representing this cube.

    If ``None``, the cube name will be used.

    :meta private:
    """

    auto_create_hierarchies: bool = True

    auto_create_measures: bool = True

    catalog_names: CubeCatalogNames = frozenset({"atoti"})
    """The names of the catalogs in which the cube will be.

    :meta private:
    """

    filter: CubeFilterCondition | None = None

    @property
    def _mode(self) -> str:
        if self.auto_create_hierarchies:
            return "AUTO" if self.auto_create_measures else "NO_MEASURES"
        if self.auto_create_measures:
            raise ValueError(
                "Cannot automatically create measures without also automatically creating hierarchies."
            )
        return "MANUAL"
