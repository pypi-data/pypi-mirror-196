from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import contactupdate as shared_contactupdate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmContactRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    contact: shared_contactupdate.ContactUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('contact') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PutCrmContactRequest:
    request: Optional[PutCrmContactRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmContactResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PutCrmContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PutCrmContactResponseBody] = dataclasses.field(default=None)
    