from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._collections import DelegatingMutableSet
from ._graphql_client import UpdateDatabaseInput
from ._identification import RoleName
from ._require_live_extension import require_live_extension


@final
class DatabaseOwners(DelegatingMutableSet[RoleName]):
    def __init__(self, *, atoti_client: AtotiClient) -> None:
        self._atoti_client: Final = atoti_client

    @override
    def _get_delegate(self) -> AbstractSet[RoleName]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        return set(graphql_client.get_database_owners().data_model.database.owners)

    @override
    def _set_delegate(self, new_set: AbstractSet[RoleName], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        mutation_input = UpdateDatabaseInput(owners=list(new_set))
        graphql_client.update_database(mutation_input)
