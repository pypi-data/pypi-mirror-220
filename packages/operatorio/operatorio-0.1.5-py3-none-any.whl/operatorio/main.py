import requests
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Union

# Models
class EntityType(Enum):
    wallet = "wallet"
    identity = "identity"
    contract = "contract"
    nft = "nft"
    token = "token"

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
    entity_type: EntityType
    query_by: List[str]

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
        query_dict = asdict(query)
        query_dict['entity_type'] = query_dict['entity_type'].value
        response = requests.post(
            OperatorSearchAPI.BASE_URL + 'search/',
            headers=headers,
            json=query_dict
        )
        
        if response.status_code == 200:
            return Entities(**response.json())
        elif response.status_code == 422:
            raise ApiException(HTTPValidationError(**response.json()))
        else:
            raise ApiException(response.json())
