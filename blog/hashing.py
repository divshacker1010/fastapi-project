from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Hash():    
    @staticmethod    
    def argon2(password: str):
        return password_hash.hash(password)