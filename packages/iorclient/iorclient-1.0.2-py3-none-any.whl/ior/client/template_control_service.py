from ..util.result_utils import error_handler,two_ret_error_handler
from rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)

class TemplateControlService(object):
    def __init__(self):
        None

    def set_api_client(self, server_url, client):
        self._api = RestAPI(api_url=server_url+"/template/control" ,driver=client)
        endpoints = [
            Endpoint(name="address",path="/get_address",method=HTTPMethod.POST),
            Endpoint(name="indexes",path="/get_indexByName",method=HTTPMethod.POST),
            Endpoint(name="templates",path="/get_templateById",method=HTTPMethod.POST),
            Endpoint(name="pay",path="/estimate_pay_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="register",path="/prepare_register_forRegister",method=HTTPMethod.POST),
            Endpoint(name="start",path="/prepare_start_forState",method=HTTPMethod.POST),
            Endpoint(name="end",path="/prepare_end_forState",method=HTTPMethod.POST),
            Endpoint(name="requestTemplate",path="/prepare_requestTemplate_forInstance",method=HTTPMethod.POST),
            Endpoint(name="tryForReceipt",path="/try_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="tryForRegister",path="/try_forRegister",method=HTTPMethod.POST),
            Endpoint(name="tryForInstance",path="/try_forInstance",method=HTTPMethod.POST),
            Endpoint(name="tryForState",path="/try_forState",method=HTTPMethod.POST),
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
    def indexes(self, service_name, _templateName):
        res = self._api.call_endpoint("indexes",data=
            {
                'name': service_name, 
                'templateName': _templateName
            })
        return res['data']

    @error_handler
    def templates(self, service_name, _templateId):
        res = self._api.call_endpoint("templates",data=
            {
                'name': service_name, 
                'templateId': _templateId
            })
        return res['data']

    @two_ret_error_handler
    def pay(self, service_name, pub, sign_func,  _templateId,_instanceId,_token,_total):
        res = self._api.call_endpoint("setAuthorizeApproval",data=
            {
                'name': service_name, 
                'templateId': _templateId, 
                'instanceId': _instanceId, 
                'tokenAddress': _token, 
                'totalIncome': _total,
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @error_handler
    def register(self, service_name, pub, sign_func,  _templateAddress,_category,_templateName,_ratio):
        res = self._api.call_endpoint("register",data=
            {
                'name': service_name, 
                'templateAddress': _templateAddress, 
                'category': _category, 
                'templateName': _templateName, 
                'ratio': _ratio,
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForRegister",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def start(self, service_name, pub, sign_func,  _templateId):
        res = self._api.call_endpoint("start",data=
            {
                'name': service_name, 
                'templateId': _templateId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForState",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res


    @error_handler
    def end(self, service_name, pub, sign_func,  _templateId):
        res = self._api.call_endpoint("end",data=
            {
                'name': service_name, 
                'templateId': _templateId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForState",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def request_template(self, service_name, pub, sign_func,  _templateId,_hash,_endTime):
        res = self._api.call_endpoint("requestTemplate",data=
            {
                'name': service_name, 
                'templateId': _templateId, 
                'hash': _hash, 
                'endTime': _endTime, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForInstance",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

