from abc import ABC
from typing import List

from external_requests.base_requests.external_request import ExternalRequest
from external_requests.request_methods import RequestMethods


class GetRequest(ExternalRequest, ABC):
    @property
    def _request_method(self) -> RequestMethods:
        return RequestMethods.GET

    @property
    def _expected_status_codes(self) -> List[int]:
        return [200]
