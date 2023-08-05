from marshmallow.schema import BaseSchema


class SerializationSchema(BaseSchema):
    _data: dict

    def __init__(self, **kwargs):
        super().__init__()
        self._data = {}
        for field in self.fields:
            self._data[field] = kwargs.pop(field)

    def serialize(self) -> dict:
        return self.dump(self._data)
