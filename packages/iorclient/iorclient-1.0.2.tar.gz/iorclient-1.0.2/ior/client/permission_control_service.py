from ..util.result_utils import error_handler,two_ret_error_handler
from rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)

class PermissionControlService(object):
    def __init__(self):
        None

    def set_api_client(self, server_url, client):
        self._api = RestAPI(api_url=server_url+"/permission/control" ,driver=client)
        endpoints = [
            Endpoint(name="address",path="/get_address",method=HTTPMethod.POST),
            Endpoint(name="hasRole",path="/has_role",method=HTTPMethod.POST),
            Endpoint(name="hasPermission",path="/has_permission",method=HTTPMethod.POST),
            Endpoint(name="datas",path="/get_dataByName",method=HTTPMethod.POST),
            Endpoint(name="grantRole",path="/estimate_grantRole_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="revokeRole",path="/estimate_revokeRole_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="addPermission",path="/estimate_addPermission_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="delPermission",path="/estimate_delPermission_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="tryForReceipt",path="/try_forReceipt",method=HTTPMethod.POST),
        ]
        self._api.register_endpoints(endpoints)

    @error_handler
    def address(self, service_name):
        res = self._api.call_endpoint("address",data=
            {
                'name': service_name
            })
        return res['data']
        
    @error_handler
    def has_role(self, service_name, _role, _to):
        res = self._api.call_endpoint("hasRole",data=
            {
                'name': service_name, 
                'role': _role, 
                'to': _to
            })
        return res['data']

    @error_handler
    def has_permission(self, service_name,  _permission, _data, _operation):
        res = self._api.call_endpoint("hasPermission",data=
            {
                'name': service_name, 
                'permission': _permission, 
                'data': _data, 
                'operation': _operation
            })
        return res['data']

    @error_handler
    def datas(self, service_name,  _data):
        res = self._api.call_endpoint("datas",data=
            {
                'name': service_name, 
                'data': _data
            })
        return res['data']


    @two_ret_error_handler
    def grant_role(self, service_name, pub, sign_func,  _role,_to):
        res = self._api.call_endpoint("grantRole",data=
            {
                'name': service_name, 
                'role': _role, 
                'to': _to, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def revoke_role(self, service_name, pub, sign_func,  _role,_to):
        res = self._api.call_endpoint("revokeRole",data=
            {
                'name': service_name, 
                'role': _role, 
                'to': _to, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def add_permission(self, service_name, pub, sign_func,  _permission,_datas,_operations,
            _defaultOperations,_parents,_hashes):
        res = self._api.call_endpoint("addPermission",data=
            {
                'name': service_name, 
                'permission': _permission, 
                'datas': _datas, 
                'operations': _operations, 
                'defaultOperations': _defaultOperations, 
                'parents': _parents, 
                'hashes': _hashes, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']


    @two_ret_error_handler
    def del_permission(self, service_name, pub, sign_func,  _permission,_datas):
        res = self._api.call_endpoint("delPermission",data=
            {
                'name': service_name, 
                'permission': _permission, 
                'datas': _datas, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

