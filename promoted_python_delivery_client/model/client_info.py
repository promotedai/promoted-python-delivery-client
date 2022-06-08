from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional
from promoted_python_delivery_client.model.client_type import ClientType

from promoted_python_delivery_client.model.traffic_type import TrafficType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ClientInfo:
    client_type: Optional[ClientType] = None
    traffic_type: Optional[TrafficType] = None
