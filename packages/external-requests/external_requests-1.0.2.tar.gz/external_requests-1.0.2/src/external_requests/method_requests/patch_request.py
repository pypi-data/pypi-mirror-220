from abc import ABC
from typing import List

from external_requests.base_requests.external_request_with_body import ExternalRequestWithBody
from external_requests.request_methods import RequestMethods


class PatchRequest(ExternalRequestWithBody, ABC):
    @property
    def _request_method(self) -> RequestMethods:
        return RequestMethods.PATCH

    @property
    def _expected_status_codes(self) -> List[int]:
        return [200]
