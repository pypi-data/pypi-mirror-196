from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import emailupdate as shared_emailupdate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmEmailRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    email: Optional[shared_emailupdate.EmailUpdate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('email'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PutCrmEmailRequest:
    request: Optional[PutCrmEmailRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmEmailResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PutCrmEmailResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PutCrmEmailResponseBody] = dataclasses.field(default=None)
    