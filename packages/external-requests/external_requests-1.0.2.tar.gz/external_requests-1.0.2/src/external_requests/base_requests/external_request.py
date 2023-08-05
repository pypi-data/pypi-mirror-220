import json

from abc import ABC, abstractmethod
from requests import Response, request
from typing import List

from external_requests.exceptions import ExternalRequestException
from external_requests.external_response import ExternalResponse
from external_requests.request_methods import RequestMethods


class ExternalRequest(ABC):
    def __init__(self, **kwargs):
        for field in kwargs:
            self.__setattr__(field, kwargs[field])

    @property
    @abstractmethod
    def _base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def _route(self) -> str:
        pass

    @property
    @abstractmethod
    def _request_method(self) -> RequestMethods:
        pass

    @property
    @abstractmethod
    def _expected_status_codes(self) -> List[int]:
        pass

    @property
    def _headers(self) -> dict:
        return {'Content-Type': 'application/json'}

    def _send_request(self, **kwargs) -> Response:
        return request(self._request_method.value, self._base_url + self._route, headers=self._headers, **kwargs)

    def request(self, **kwargs) -> ExternalResponse:
        try:
            response: Response = self._send_request(**kwargs)
        except Exception as e:
            raise ExternalRequestException(f'Failed to send a request to {self._base_url + self._route}. '
                                           f'Error - {str(e)}')
        else:
            if response.status_code not in self._expected_status_codes:
                raise ExternalRequestException(f'Received unexpected status code {response.status_code}. '
                                               f'Reason - {response.text}')

            return ExternalResponse(json.loads(response.content), response.status_code)
