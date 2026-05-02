from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Hash():    
    @staticmethod    
    def argon2(password: str):
        return password_hash.hash(password)
    @staticmethod
    def verify(plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)