import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Users:
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
        
    def batch(self, request: operations.GetBatchCrmUserRequest) -> operations.GetBatchCrmUserResponse:
        r"""Get Batch Users
        Retrieve Users by a set of Id's
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/user/batch'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetBatchCrmUserResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetBatchCrmUserResponseBody])
                res.response_body = out

        return res

    def details(self, request: operations.GetDetailsCrmUserRequest) -> operations.GetDetailsCrmUserResponse:
        r"""Get User Details
        Get details about all users. 
        Details include the type, possible values, and other meta data about the fields.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/user/details'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetDetailsCrmUserResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetDetailsCrmUserResponseBody])
                res.response_body = out

        return res

    def find(self, request: operations.GetOneCrmUserRequest) -> operations.GetOneCrmUserResponse:
        r"""Get User
        Retrieve a single User by Id
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/user'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetOneCrmUserResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetOneCrmUserResponseBody])
                res.response_body = out

        return res

    def list(self, request: operations.GetAllCrmUsersRequest) -> operations.GetAllCrmUsersResponse:
        r"""Get All Users
        Retrieve all Users
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/users'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetAllCrmUsersResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetAllCrmUsersResponseBody])
                res.response_body = out

        return res

    def search(self, request: operations.SearchCrmUsersRequest) -> operations.SearchCrmUsersResponse:
        r"""Search Users
        Search all Users using filters
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/users/search'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('POST', url, params=query_params, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.SearchCrmUsersResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.SearchCrmUsersResponseBody])
                res.response_body = out

        return res

    