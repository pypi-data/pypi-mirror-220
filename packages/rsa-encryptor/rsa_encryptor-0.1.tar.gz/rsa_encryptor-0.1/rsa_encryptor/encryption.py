import rsa
import base64
from os import path
from .keygen import KeyGen

class Encryption(KeyGen):
    
    __block_size = None
    __cipher_length = None
    
    
    def __init__(self, key_size=512, pool_size=8, output_dir='./storage', pb_alias="public_key", pr_alias="private_key") -> None:
        super().__init__(key_size, pool_size, output_dir, pb_alias, pr_alias)
        self.__block_size = (key_size // 8) - 11
        self.__cipher_length = key_size // 8
        
    
    """
    Encrypts given message using public_key

    Parameters:
    message (str): The message to be encrypted.

    Returns:
    str: Base64 encrypted message.
    """
    def encrypt_message(self,message='',plain=True):
        if not self.public_key:
            raise ValueError("No public key, please generate or load one.")
        if not message:
            return None
        
        encoded_text = message.encode('utf-8') if type(message) != bytes else message
        encrypted = []
        if len(encoded_text) > self.__block_size:
            blocks = [encoded_text[i:i+self.__block_size] for i in range(0, len(encoded_text), self.__block_size)]
            
            encrypted = [rsa.encrypt(block,self.public_key) for block in blocks]
        else:
            encrypted = [rsa.encrypt(encoded_text,self.public_key)]
            
        data = b''
        for block in encrypted:
            data += block 
        
        try:
            return base64.b64encode(data) if not plain else base64.b64encode(data).decode('utf-8')
        except UnicodeDecodeError:
            return data
            

     
    """
    Decrypts a given message using private_key

    Parameters:
    message (str): The message to be decrypted.

    Returns:
    str: Decrypted message.
    """
    def decrypt_message(self,encrypted_message=b''):
        if not self.private_key:
            raise ValueError("No private key, please generate or load one.")
        if not encrypted_message or type(encrypted_message)!= bytes:
            raise TypeError(f"encrypted_message must be bytes not {type(encrypted_message)}")
        
        decrypted = []
        
        encrypted_message = base64.b64decode(encrypted_message)
        
        if len(encrypted_message) > self.__cipher_length:
            blocks = [encrypted_message[i:i+self.__cipher_length] for i in range(0, len(encrypted_message), self.__cipher_length)]

            decrypted = [rsa.decrypt(block,self.private_key) for block in blocks]
        else:
            decrypted = [rsa.decrypt(encrypted_message,self.private_key)]
        
        data = b''
        for block in decrypted:
            data += block
        
        return data
        
    """
    Encrypts a given file using public_key

    Parameters:
    file_path(str): The path to file.

    """
    def encrypt_file(self,file_path):
        if not self.public_key:
            raise ValueError("No public key, please generate or load one.")
        
        with open(file_path,'rb') as f:
            contents = f.read()
            file_name = f.name
        
        encrypted = self.encrypt_message(contents,plain=False)
        with open(path.join(self.output_dir,f"encrypted_{path.basename(file_name)}"),'wb') as f:
            f.write(encrypted)
            
    """
    Decrypts given file using private_key

    Parameters:
    file_path(str): The path to file.

    """
    def decrypt_file(self,file_path):
        if not self.private_key:
            raise ValueError("No private key, please generate or load one.")
        
        with open(file_path,'rb') as f:
            encrypted = f.read()
        decrypted = self.decrypt_message(encrypted_message=encrypted)
        
        with open(path.join(self.output_dir,f"{path.basename(file_path).split('encrypted_')[1]}"),'wb') as f:
            f.write(decrypted)

