from typing import Any

from ..api import RequestService
from ..endpoints import GenericPluralEndpoint


class LocationsEndPoint(GenericPluralEndpoint):
    def __init__(self, request_service: RequestService, identifier: Any = None):
        super(LocationsEndPoint, self).__init__(request_service=request_service)
        self._endpoint = "/api/v2/locations"
        self.plural_resource_key = "locations"
        self.single_resource_key = "location"
        self.identifier = identifier
