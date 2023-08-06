import requests
from dataclasses import dataclass
from typing import List, Union

# Models
@dataclass
class Entity:
    address: str
    description: str
    semantic_similarity: float
    network_value: float = 0.0
    rank: float = 0.0

@dataclass
class Entities:
    entity: str
    matches: List[Entity]

@dataclass
class Query:
    query: str
    blockchain: str
    entity_type: str

@dataclass
class ValidationError:
    loc: List[Union[str, int]]
    msg: str
    type: str

@dataclass
class HTTPValidationError:
    detail: List[ValidationError]

# Exception
class ApiException(Exception):
    def __init__(self, payload):
        self.payload = payload
        super().__init__(self.message)

    @property
    def message(self):
        return str(self.payload)

class OperatorSearchAPI:
    BASE_URL = 'https://api.operator.io/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: Query) -> Entities:
        headers = {"X-API-Key": self.api_key}
        response = requests.post(
            OperatorSearchAPI.BASE_URL + '/search/',
            headers=headers,
            json=query.__dict__
        )
        
        if response.status_code == 200:
            return Entities(**response.json())
        else:
            raise ApiException(response.json())
