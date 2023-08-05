from typing import Any


class ExternalResponse:
    def __init__(self, data: Any, status: int):
        self.data = data
        self.status = status
