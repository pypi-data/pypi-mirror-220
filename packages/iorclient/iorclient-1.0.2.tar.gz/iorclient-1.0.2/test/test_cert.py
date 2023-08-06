from ior.iorsdk import IORClient
from ior.util.web3_utils import keccak256
import unittest

class TestCertMethods(unittest.TestCase):
    def setUp(self):
        #main test for example        
        self.ior = IORClient("http://121.5.19.151:8199/tzspace/v1/api")
        self.ior.init_w3()
        self.ior.init_apis()

        self.pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
        self.pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

        pub1,pk1 = self.ior.create_account()
        pub2,pk2 = self.ior.create_account()
        pub3,pk3 = self.ior.create_account()

        self.pubs = [self.pub,pub1,pub2,pub3]
        self.pks = {self.pub:self.pk,pub1:pk1,pub2:pk2,pub3:pk3}

    def test_cert(self):
        
        def sign_tx(pub,tx):
            stx = self.ior.sign_transaction(tx,self.pks[pub])
            return stx.rawTransaction.hex()

        pub = self.pubs[0]
        cert = self.ior.get('cert')

        ret,certId = cert.mint('stcc',pub,sign_tx, pub)
        print('mint',ret,certId)
        
        hashValue = keccak256('cert').hex()
        ret,res,receipt = cert.update_hash('stcc',pub,sign_tx, certId,hashValue)
        print('update_hash',res)

        hashValue = keccak256('cert2').hex()
        ret,res = cert.verify_hash('stcc',certId,hashValue)
        print('verify_hash',res)

        ret,res = cert.pretokens('stcc',certId)
        print('pretokens',res)

        ret,res,receipt = cert.set_authorize_approval('stcc',pub,sign_tx, certId,self.pubs[1],True)
        print(res)
        ret,res = cert.is_authorize_approved('stcc', certId,self.pubs[1])
        print(res)
        ret,nId = cert.authorize('stcc',self.pubs[1],sign_tx, self.pubs[2],certId)
        print(nId)
        ret,nxId = cert.pretokens('stcc',nId)
        print('pretokens',nxId)
        ret,res = cert.safe_transfer_from('stcc',self.pubs[2],sign_tx, self.pubs[2],self.pubs[3],nId)
        print(res)


 
if __name__=='__main__':
    unittest.main()
