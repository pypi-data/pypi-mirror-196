from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import notecreate as shared_notecreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmNoteRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    note: shared_notecreate.NoteCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('note') }})
    

@dataclasses.dataclass
class PostCrmNoteRequest:
    request: Optional[PostCrmNoteRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmNoteResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PostCrmNoteResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PostCrmNoteResponseBody] = dataclasses.field(default=None)
    