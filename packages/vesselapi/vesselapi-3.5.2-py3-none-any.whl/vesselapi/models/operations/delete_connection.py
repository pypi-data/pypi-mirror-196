from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import security as shared_security
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class DeleteConnectionSecurity:
    vessel_api_token: shared_security.SchemeVesselAPIToken = dataclasses.field(metadata={'security': { 'scheme': True, 'type': 'apiKey', 'sub_type': 'header' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class DeleteConnectionRequestBody:
    connection_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('connectionId') }})
    

@dataclasses.dataclass
class DeleteConnectionRequest:
    security: DeleteConnectionSecurity = dataclasses.field()
    request: Optional[DeleteConnectionRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class DeleteConnectionResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    