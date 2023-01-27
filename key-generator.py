from cryptography.fernet import Fernet


f = open('key.txt' , 'w')
chiave_fernet = Fernet.generate_key()
chiave_fernet = chiave_fernet.decode('utf-8')
f.write(chiave_fernet)
f.close()
