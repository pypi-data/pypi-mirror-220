from ior.iorsdk import IORClient
from ior.util.web3_utils import keccak256
import unittest

class TestRoleMethods(unittest.TestCase):
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

    def test_role(self):
        
        def sign_tx(pub,tx):
            stx = self.ior.sign_transaction(tx,self.pks[pub])
            return stx.rawTransaction.hex()

        pub = self.pubs[0]
        rolectrl = self.ior.get('role')
        pctrl = self.ior.get('permission')

        permission = "AddData"
        permissions = [permission]
        roleName = "Role1"
        adminRoleName = "AdminRole"
        permissionRoleName = "PermissionRole"

        ret,addr = pctrl.address('pctrl')
        permissionContractAddrs = [addr]

        #只需要添加一次
        ret,res,receipt = rolectrl.add_role('rolectrl',pub,sign_tx, roleName,adminRoleName,permissionRoleName,permissions,permissionContractAddrs)
        print('add_role', res)
        ret,res = rolectrl.roles('rolectrl', keccak256(roleName).hex())
        print('roles', res)
        ret,res,receipt = rolectrl.grant_role('rolectrl',pub,sign_tx, adminRoleName,self.pubs[1])
        ret,res,receipt = rolectrl.grant_role('rolectrl',self.pubs[1],sign_tx, permissionRoleName,self.pubs[2])
        ret,res,receipt = rolectrl.grant_role('rolectrl',self.pubs[1],sign_tx, roleName,self.pubs[3])
        print('grant all roles',res)
        permissionAdmin = "AdminRole"
        ret,res,receipt = pctrl.grant_role('pctrl',pub,sign_tx, permissionAdmin,self.pubs[2])
        print('grant first permission',res)

        permissionAdmin2 = "AdminRole2"
        ret,res,receipt = pctrl.grant_role('pctrl',pub,sign_tx, permissionAdmin2,self.pubs[2])
        print('grant all permission',ret)

        ret,res,receipt = rolectrl.add_permission('rolectrl',self.pubs[2],sign_tx, roleName,permissions,permissionContractAddrs)
        
        #read 0x01, write 0x02, read and write 0x03
        data = ["username","idcard"]
        operations = [0x02,0x03]
        defaultOperations = [0x01,0x02]
        parent = ["1.2.121.1.3.21.2","1.2.121.1.3.21.2"]
        dhash = data;

        ret,res,receipt = pctrl.add_permission('pctrl',self.pubs[2],sign_tx, permission,data,operations,defaultOperations,parent,dhash)
       
        data1 = "username"
        operation = 0x02
        ret,res = rolectrl.has_permission('rolectrl',roleName,permission,data1,operation)
        print(res, roleName, permission, data1, operation)

        operation0 = 0x02
        ret,res = pctrl.has_permission('pctrl',permission,data1,operation0)
        print(res)

        data2 = "idcard"
        operation2 = 0x02
        ret,res = rolectrl.has_permission('rolectrl',roleName,permission,data2,operation2)
        print(res)

        operation3 = 0x01
        ret,res = rolectrl.has_permission('rolectrl',roleName,permission,data2,operation3)
        print(res)

        ret,res,receipt = rolectrl.del_permission('rolectrl',self.pubs[2],sign_tx, roleName,[permission])
        
        operation4 = 0x01
        ret,res = rolectrl.has_permission('rolectrl',roleName,permission,data1,operation4)
        print(res)


 
if __name__=='__main__':
    unittest.main()
