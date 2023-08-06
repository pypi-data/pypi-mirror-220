from typing import Any

from ..api import RequestService
from ..endpoints import GenericPluralEndpoint


class AssetTypeEndPoint(GenericPluralEndpoint):
    def __init__(self, request_service: RequestService, identifier: Any = None):
        super(AssetTypeEndPoint, self).__init__(request_service=request_service)
        self._endpoint = "/api/v2/asset_types"
        self.plural_resource_key = "asset_types"
        self.single_resource_key = "asset_type"
        self.identifier = identifier
