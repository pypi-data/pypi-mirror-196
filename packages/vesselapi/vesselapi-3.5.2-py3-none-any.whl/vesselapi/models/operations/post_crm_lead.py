from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import leadcreate as shared_leadcreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmLeadRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    lead: shared_leadcreate.LeadCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('lead') }})
    

@dataclasses.dataclass
class PostCrmLeadRequest:
    request: Optional[PostCrmLeadRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmLeadResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PostCrmLeadResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PostCrmLeadResponseBody] = dataclasses.field(default=None)
    