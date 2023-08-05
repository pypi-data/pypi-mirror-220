
from rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)

class ContractTemplateService(object):
    def __init__(self):
        None

    def set_api_client(self, server_url, client):
        self._api = RestAPI(api_url=server_url+"/contract/template" ,driver=client)
        endpoints = [
            Endpoint(name="canPay",path="/can_pay",method=HTTPMethod.POST),
            Endpoint(name="getPayees",path="/get_payees",method=HTTPMethod.POST),
            Endpoint(name="getRatioByPayee",path="/get_ratioByPayee",method=HTTPMethod.POST),
            Endpoint(name="init",path="/estimate_init_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="sign",path="/prepare_sign_forSign",method=HTTPMethod.POST),
            Endpoint(name="start",path="/prepare_start_forState",method=HTTPMethod.POST),
            Endpoint(name="end",path="/prepare_end_forState",method=HTTPMethod.POST),
            Endpoint(name="tryForReceipt",path="/try_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="tryForSign",path="/try_forSign",method=HTTPMethod.POST),
            Endpoint(name="tryForState",path="/try_forState",method=HTTPMethod.POST),
        ]
        self._api.register_endpoints(endpoints)

    def can_pay(self, service_name, _instanceId, _payerAddress):
        res = self._api.call_endpoint("canPay",data=
            {
                'name': service_name, 
                'instanceId': _instanceId,
                'payerAddress': _payerAddress
            })
        return res['data']

    def get_payees(self, service_name, _instanceId):
        res = self._api.call_endpoint("getPayees",data=
            {
                'name': service_name, 
                'instanceId': _instanceId
            })
        return res['data']


    def get_ratio_by_payee(self, service_name, _instanceId, _payee):
        res = self._api.call_endpoint("getRatioByPayee",data=
            {
                'name': service_name,
                'instanceId': _instanceId, 
                'payee': _payee
            })
        return res['data']

    def init(self, service_name, pub, sign_func,  _instanceId,_signatories,_payer,_payees,_shareRatios):
        res = self._api.call_endpoint("init",data=
            {
                'name': service_name, 
                'instanceId': _instanceId, 
                'signatories': _signatories, 
                'payer': _payer, 
                'payees': _payees, 
                'shareRatios': _shareRatios, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    def start(self, service_name, pub, sign_func,  _instanceId):
        res = self._api.call_endpoint("start",data=
            {
                'name': service_name, 
                'instanceId': _instanceId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForState",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res


    def end(self, service_name, pub, sign_func,  _instanceId):
        res = self._api.call_endpoint("end",data=
            {
                'name': service_name, 
                'instanceId': _instanceId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForState",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    def sign(self, service_name, pub, sign_func,  _instanceId):
        res = self._api.call_endpoint("sign",data=
            {
                'name': service_name, 
                'instanceId': _instanceId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForSign",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

