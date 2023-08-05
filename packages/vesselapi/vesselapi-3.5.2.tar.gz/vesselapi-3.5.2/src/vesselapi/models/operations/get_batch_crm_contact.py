from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import contact as shared_contact
from dataclasses_json import Undefined, dataclass_json
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class GetBatchCrmContactQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    ids: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'ids', 'style': 'form', 'explode': True }})
    

@dataclasses.dataclass
class GetBatchCrmContactRequest:
    query_params: GetBatchCrmContactQueryParams = dataclasses.field()
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class GetBatchCrmContactResponseBody:
    contacts: Optional[list[shared_contact.Contact]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('contacts'), 'exclude': lambda f: f is None }})
    invalid_ids: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('invalidIds'), 'exclude': lambda f: f is None }})
    

@dataclasses.dataclass
class GetBatchCrmContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[GetBatchCrmContactResponseBody] = dataclasses.field(default=None)
    