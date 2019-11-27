from modules.Ciphers import POO_RSA

def check(pub_key):

    rsa = POO_RSA.main()

    try:

        rsa.import_PublicKey(pub_key)

    except ValueError:

        return(False)

    except POO_RSA.privateKeyFound:

        return(-1)

    else:

        return(True)
