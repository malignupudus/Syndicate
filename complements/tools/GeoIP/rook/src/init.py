from requests import get

def geolocation():

    ip = get('https://ifconfig.me').content
    ip = ip.decode() if (isinstance(ip, bytes)) else str(ip)

    return(ip)
