import rsa
import base64
from os import path
from .keygen import KeyGen

class Signature(KeyGen):
    
    def sign(self,file_path):
        
        if not self.private_key:
            raise ValueError("No private key, please generate or load one.")
        if not file_path:
            return None
        
        with open(file_path,'rb') as f:
            contents = f.read()
            
        signature = base64.b64encode(rsa.sign(contents,self.private_key,'SHA-256')).decode()
        print(self.output_dir)
        with open(path.join(self.output_dir,f"{path.splitext(path.basename(file_path))[0]}_Signature.sgn"),'w') as f:
            f.write(signature)
            
            
    def verify(self,file_path,signature_path):
        
        if not self.public_key:
            raise ValueError("No public key, please generate or load one.")
        if not (file_path or signature_path):
            raise ValueError("You should provide the file_path and signature file path to verify the signature")
        
        with open(file_path, 'rb') as f:
            contents = f.read()
            
        with open(signature_path, 'r') as f:
            signature = f.read()
            
        try:
            rsa.verify(contents,base64.b64decode(signature),self.public_key)
            print("Verification Completed, file is authentic")
            return True
        except:
            print("Cannot verify the file, it maybe altered or is not from alleged sender")
            return False
            
        
signer = Signature()