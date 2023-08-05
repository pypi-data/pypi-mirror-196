from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import noteupdate as shared_noteupdate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmNoteRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    note: shared_noteupdate.NoteUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('note') }})
    

@dataclasses.dataclass
class PutCrmNoteRequest:
    request: Optional[PutCrmNoteRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PutCrmNoteResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PutCrmNoteResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PutCrmNoteResponseBody] = dataclasses.field(default=None)
    