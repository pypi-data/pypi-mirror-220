# External Requests
A class based alternative to making HTTP requests in Python.

### Installation
Installation can be done with pip:
```
pip install external-requests
```

### Basic Usage
In order to use external requests, you must implement one of the abstract classes provided by the package, create an 
instance of your new class, and call the request function.

```python
from typing import List
from external_requests.base_requests.external_request import ExternalRequest
from external_requests.request_methods import RequestMethods


class ExampleRequest(ExternalRequest):
    @property
    def _base_url(self) -> str:
        return 'http://some-url.com'

    @property
    def _route(self) -> str:
        return '/my-route'

    @property
    def _request_method(self) -> RequestMethods:
        return RequestMethods.GET

    @property
    def _expected_status_codes(self) -> List[int]:
        return [200]
        
ExampleRequest().request()
```
Want to avoid duplication between similar requests? You can replace the ExternalRequest base class with one of
the alternative, request-specific classes which implement both the request method and expected status code properties.
There is a request-specific class for all seven primary HTTP request methods: GET, POST, PUT, PATCH, DELETE, HEAD 
and OPTIONS.

### Working With Parameters
Parameters can be injected into the request when creating an instance of it. This is done using kwargs which are saved
on the object in the __init__ function by default. It is recommended that you also state the parameters on the 
class for readability, although this is not required.
```python
from external_requests.method_requests.get_request import GetRequest

class ExampleRequest(GetRequest):
    route_param: str

    @property
    def _base_url(self) -> str:
        return 'http://some-url.com'

    @property
    def _route(self) -> str:
        return f'/my-route/{self.route_param}'
        
ExampleRequest(route_param='value').request()
```

### Requests With Bodies
In order to both simplify and create standardization in requests with bodies, the SerializationSchema class 
(based on marshmallow) is available. In order to use it, simply create an instance of your needed schema, inherit from
SerializationSchema, and return an instance of your schema in your request's _body_schema property.
```python
from marshmallow import fields
from external_requests.method_requests.post_request import PostRequest
from external_requests.serialization_schema import SerializationSchema


class ExampleSchema(SerializationSchema):
    name = fields.Str(data_key='name')
    other_attribute = fields.Str(data_key='otherAttribute')
    

class ExampleRequest(PostRequest):
    name: str
    other_attribute: str

    @property
    def _body_schema(self) -> SerializationSchema:
        return ExampleSchema(name=self.name, other_attribute=self.other_attribute)

    @property
    def _base_url(self) -> str:
        return 'http://some-url.com'

    @property
    def _route(self) -> str:
        return '/my-route'
    
ExampleRequest(name='name', other_attribute='other').request()
```

The project's code can be found here https://gitlab.com/VenfiOranai/external-requests
