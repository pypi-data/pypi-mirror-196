from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import dealcreate as shared_dealcreate
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmDealRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    deal: shared_dealcreate.DealCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('deal') }})
    

@dataclasses.dataclass
class PostCrmDealRequest:
    request: Optional[PostCrmDealRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostCrmDealResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    

@dataclasses.dataclass
class PostCrmDealResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PostCrmDealResponseBody] = dataclasses.field(default=None)
    