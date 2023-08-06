
from .util.web3_utils import get_web3, create_account
from .util.web3_utils import util_send_raw_transaction, util_estimate_transaction, util_sign_transaction
from .client.template_control_service import TemplateControlService
from .client.certificate_service import CertificateService
from .client.exchange_service import ExchangeService
from .client.permission_control_service import PermissionControlService
from .client.role_control_service import RoleControlService
from .client.contract_template_service import ContractTemplateService
import traceback
import httpx

from hexbytes import (
    HexBytes,
)

def error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            return func(self,*args,**kwargs), 0
        except:
            msg = traceback.format_exc()
            return f'error:{msg}', 1
    return execute

class IORClient(object):
	_services = {}

	def __init__(self, server_url, is_print=False):
		self._server_url = server_url
		self._is_print = is_print
		self._client = httpx.Client()

	def init_w3(self, provider=None, is_poa=False):	
		self._w3 = get_web3(provider, self._is_print, is_poa)

	def init_apis(self):	
		self.set('cert',CertificateService())
		self.set('exchnage',ExchangeService())
		self.set('permission',PermissionControlService())
		self.set('role',RoleControlService())
		self.set('template',TemplateControlService())
		self.set('ctrt',ContractTemplateService())

	@property
	def w3(self):
		return self._w3

	def set(self, name, service):
		service.set_api_client(self._server_url, self._client)
		self._services[name] = service

	def get(self, name):
		if name not in self._services:
			return None
		return self._services[name]

	def create_account(self):
		return create_account(self.w3)

	@error_handler
	def deploy_transaction(self, rawTx):
		receipt = util_send_raw_transaction(self.w3, rawTx, self._config.timeout, self._config.poll_latency)
		return receipt.contractAddress

	@error_handler
	def execute_transaction(self, rawTx):
		receipt = util_send_raw_transaction(self.w3, rawTx, self._config.timeout, self._config.poll_latency)
		return receipt

	def sign_transaction(self, tx, private_key):
		signed_tx = util_sign_transaction(self.w3, tx, private_key)
		return signed_tx
