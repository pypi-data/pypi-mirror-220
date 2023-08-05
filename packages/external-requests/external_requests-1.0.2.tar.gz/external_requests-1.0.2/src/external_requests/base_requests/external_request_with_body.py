import json

from abc import ABC, abstractmethod
from requests import Response, request

from external_requests.base_requests.external_request import ExternalRequest
from external_requests.serialization_schema import SerializationSchema


class ExternalRequestWithBody(ExternalRequest, ABC):
    @property
    @abstractmethod
    def _body_schema(self) -> SerializationSchema:
        pass

    def _send_request(self, **kwargs) -> Response:
        return request(self._request_method.value, self._base_url + self._route, headers=self._headers,
                       data=json.dumps(self._body_schema.serialize()), **kwargs)
