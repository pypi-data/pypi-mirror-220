from abc import ABC

from external_requests.base_requests.external_request import ExternalRequest
from external_requests.request_methods import RequestMethods


class HeadRequest(ExternalRequest, ABC):
    @property
    def _request_method(self) -> RequestMethods:
        return RequestMethods.HEAD
