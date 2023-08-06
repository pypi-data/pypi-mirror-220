import rsa
from os import path, mkdir
from pathlib import Path

class KeyGen:
    
    __public_key = None
    __private_key = None
    
    def __init__(self,key_size=512,pool_size=8,output_dir=path.join(Path(__file__).resolve().parent.parent,'storage'),pb_alias="public_key",pr_alias="private_key") -> None:
        self.key_size= key_size
        self.pool_size = pool_size
        self.output_dir = output_dir
        self.pb_alias = pb_alias
        self.pr_alias = pr_alias
        if not path.exists(self.output_dir):
            try:
                mkdir(self.output_dir)
            except:
                pass
        
    """
    Generates a pair of public/private key
   
    """
    def generate_key_pair(self):
        public_key,private_key = rsa.newkeys(self.key_size,self.pool_size)
        self.__public_key= public_key
        self.__private_key = private_key
        
    """
    Exports generated keys in pem file format

    """
    def export_keys(self):
        if not (self.__private_key or self.__public_key):
            raise ValueError("You have to generate the keys before exporting them, Use generate_key_pair to generate them.")
        
        with open(path.join(self.output_dir,f"{self.pb_alias}.pem"),'wb') as f:
            f.write(self.__public_key._save_pkcs1_pem())
        
        with open(path.join(self.output_dir,f"{self.pr_alias}.pem"),'wb') as f:
            f.write(self.__private_key._save_pkcs1_pem())
    
    
    """
    Loads private or public keys from .pem format
    
    Parameters:
    private_key_path (str): The path to private_key.pem.
    public_key_path (str): The path to public_key.pem.

    """
    def load_keys(self, private_key_path=None, public_key_path=None):
        if not (private_key_path or public_key_path):
            raise TypeError("Passing at least one argument is required!")

        if private_key_path:
            with open(private_key_path,'rb') as f:
                private_key_data = f.read()
                
            self.__private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
            
            
        if public_key_path:
            with open(public_key_path,'rb') as f:
                public_key_data = f.read()
                
            self.__public_key = rsa.PublicKey.load_pkcs1(public_key_data)
            
    @property
    def public_key(self):
        return self.__public_key
    
    @property
    def private_key(self):
        return self.__private_key
    