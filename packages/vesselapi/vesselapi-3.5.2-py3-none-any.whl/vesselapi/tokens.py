import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Tokens:
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
        
    def create(self, request: operations.PostLinkTokenRequest) -> operations.PostLinkTokenResponse:
        r"""Create Link Token
        Generates a link token to be used during the authentication flow. This token is passed to either the Vessel Link Component or `useVesselLink` hook.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/link/token'
        
        
        client = utils.configure_security_client(self._client, request.security)
        
        http_res = client.request('POST', url)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PostLinkTokenResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PostLinkTokenResponseBody])
                res.response_body = out

        return res

    