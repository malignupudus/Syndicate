from modules.Ciphers import POO_RSA

def _decrypt(priv_key, password):

    rsa = POO_RSA.main()

    rsa.import_PrivateKey(priv_key, password)

    return(rsa.export_PrivateKey())
