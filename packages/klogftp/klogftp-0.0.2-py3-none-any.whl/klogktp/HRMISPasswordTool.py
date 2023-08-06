from Crypto.Cipher import AES

class HRMISPasswordTool:

    def __init__(self, **kwargs) -> None:
        self.secret_key = b'^!(@!)~*@)!*@222' # default secret_key
        if 'secret_key' in kwargs:
            if type(kwargs['secret_key']) == str:
                secret_key = kwargs['secret_key'].encode('utf-8')
                secret_key = self.splice(secret_key)
                self.secret_key = secret_key
            elif type(kwargs['secret_key']) == bytes:
                secret_key = self.splice(kwargs['secret_key'])
                self.secret_key = secret_key
                
        self.aes = AES.new(self.secret_key, AES.MODE_ECB)

    def splice(self, key):
        while len(key) % 16 != 0:
            key += b' '
        return key

    def Encrypt(self, plaintext:bytes or str) -> bytes:
        if type(plaintext) == bytes:
            encrypted_byte = self.aes.encrypt(self.splice(plaintext))
            encrypted_byte = encrypted_byte.hex()
            # print(f"encrypted_byte: {encrypted_byte}")
            return encrypted_byte
        elif type(plaintext) == str:
            plaintext = plaintext.encode('utf-8')
            encrypted_byte = self.aes.encrypt(self.splice(plaintext))
            encrypted_byte = encrypted_byte.hex()
            return encrypted_byte
            
    def Decrypt(self, encrypted_byte:bytes or str) -> bytes:
        if type(encrypted_byte) == bytes:
            descrypted_byte = self.aes.decrypt(encrypted_byte).decode('utf-8').rstrip(' ')
            # print(f"descrypted_byte: {descrypted_byte}")
            return descrypted_byte
        elif type(encrypted_byte) == str:
            encrypted_byte = bytes.fromhex(encrypted_byte)
            descrypted_byte = self.aes.decrypt(encrypted_byte).decode('utf-8').rstrip(' ')
            # print(f"descrypted_byte: {descrypted_byte}")
            return descrypted_byte
        # return plaintext
        # plaintext = strText.encode('utf-8')
        # cipher.decrypt(plaintext)