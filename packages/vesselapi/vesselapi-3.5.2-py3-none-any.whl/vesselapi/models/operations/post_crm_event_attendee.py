from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import eventattendeecreate as shared_eventattendeecreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmEventAttendeeResponseBody:
    access_token: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken'), 'exclude': lambda f: f is None }})
    event_attendee: Optional[shared_eventattendeecreate.EventAttendeeCreate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('eventAttendee'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class PostCrmEventAttendeeResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PostCrmEventAttendeeResponseBody] = dataclasses.field(default=None)
    