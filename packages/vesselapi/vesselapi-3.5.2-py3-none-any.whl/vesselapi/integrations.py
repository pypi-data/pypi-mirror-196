import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Integrations:
    _client: requests_http.Session
    _security_client: requests_http.Session
    _server_url: str
    _language: str
    _sdk_version: str
    _gen_version: str

    def __init__(self, client: requests_http.Session, security_client: requests_http.Session, server_url: str, language: str, sdk_version: str, gen_version: str) -> None:
        self._client = client
        self._security_client = security_client
        self._server_url = server_url
        self._language = language
        self._sdk_version = sdk_version
        self._gen_version = gen_version
        
    def list(self) -> operations.GetAllCrmIntegrationsResponse:
        r"""Get CRM Integrations
        Return all of the CRM integrations supported by Vessel.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/connection/crm/integrations'
        
        
        client = self._security_client
        
        http_res = client.request('GET', url)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetAllCrmIntegrationsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetAllCrmIntegrationsResponseBody])
                res.response_body = out

        return res

    