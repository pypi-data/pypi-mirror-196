def enc(url):
    from cryptography.fernet import Fernet
    Key = Fernet(b'r-gVyaKFrzE66xFYBpigvh83HpgTBPKxoG4oXLDJN9M=')
    with open(url,"rb") as File:
        Data = File.read()
        EncryptedData = Key.encrypt(Data)
        with open(url,"wb") as File:
            File = File.write(EncryptedData)

def dec(url):
    from cryptography.fernet import Fernet
    Key = Fernet(b'r-gVyaKFrzE66xFYBpigvh83HpgTBPKxoG4oXLDJN9M=')
    with open(url,"rb") as File:
        Data = File.read()
        DecryptedData = Key.decrypt(Data)
        with open(url,"wb") as File:
            File = File.write(DecryptedData)