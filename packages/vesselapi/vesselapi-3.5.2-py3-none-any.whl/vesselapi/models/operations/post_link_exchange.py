from __future__ import annotations
import dataclasses
import requests as requests_http
from ..shared import security as shared_security
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from vesselapi import utils


@dataclasses.dataclass
class PostLinkExchangeSecurity:
    vessel_api_token: shared_security.SchemeVesselAPIToken = dataclasses.field(metadata={'security': { 'scheme': True, 'type': 'apiKey', 'sub_type': 'header' }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostLinkExchangeRequestBody:
    public_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('publicToken') }})
    

@dataclasses.dataclass
class PostLinkExchangeRequest:
    security: PostLinkExchangeSecurity = dataclasses.field()
    request: Optional[PostLinkExchangeRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    
class PostLinkExchangeResponseBodyIntegrationIDEnum(str, Enum):
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    PIPEDRIVE = "pipedrive"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PostLinkExchangeResponseBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('accessToken') }})
    connection_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('connectionId') }})
    integration_id: PostLinkExchangeResponseBodyIntegrationIDEnum = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('integrationId') }})
    native_org_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('nativeOrgId') }})
    native_org_url: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('nativeOrgURL') }})
    

@dataclasses.dataclass
class PostLinkExchangeResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    raw_response: Optional[requests_http.Response] = dataclasses.field(default=None)
    response_body: Optional[PostLinkExchangeResponseBody] = dataclasses.field(default=None)
    