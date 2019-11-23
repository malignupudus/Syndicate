import json
from requests import get
from hashlib import md5

from utils.sys_utils import bytes_convert
from utils.UI import debug
from utils.UI import evieModule

def main(result, log, args):

    wrap = evieModule.CreateDatabase('GeoIP')
    rhost = str(result)

    log.logger('Tratando de localizar a: "{}"'.format(rhost), debug.WAR)

    try:

        data = get('http://ip-api.com/json/{}'.format(rhost)).json()

    except json.decoder.JSONDecodeError:

        log.logger('Error descodificando los datos al intentar localizar a: "{}"'.format(rhost), debug.WAR)

    except Exception as Except:

        log.logger('Ocurrio una excepción conectando a la API para localizar a: "{}"'.format(rhost), debug.WAR)

    else:

        if not (data['status'] == 'fail'):
        
            print('\033[1;34m* \033[37mInformación obtenida de \033[0m"\033[1;4;37m{}\033[0m" \033[1;34m*\033[0m'.format(data['query']))
            print()
            print('\033[1;34mPaís: \033[32m{}'.format(data['country']))
            print('\033[1;34mCiudad: \033[32m{}'.format(data['city']))
            print('\033[1;34mCódigo del País: \033[32m{}'.format(data['countryCode']))
            print('\033[1;34mProveedor de Servicios: \033[32m{}'.format(data['isp']))
            print('\033[1;34mRegión: \033[32m{}'.format(data['region']))
            print('\033[1;34mNombre de la región: \033[32m{}'.format(data['regionName']))
            print('\033[1;34mOrganización: \033[32m{}'.format(data['org']))
            print('\033[1;34mAsociación: \033[32m{}'.format(data['as']))
            print('\033[1;34mZona Horaria: \033[32m{}'.format(data['timezone']))
            print('\033[1;34mLatitud: \033[32m{}'.format(data['lat']))
            print('\033[1;34mLongitud: \033[32m{}'.format(data['lon'])) 
            print('\033[1;34mMapa de Google: \033[32m{}\033[0m'.format('https://www.google.com/maps/place/\033[31m{0}\033[0;1;32m,\033[31m{1}\033[0;1;32m/@\033[31m{0}\033[0;1;32m,\033[31m{1}\033[0;1;32m,16z\033[0m'.format(data['lat'], data['lon'])))

            log.logger('Almacenando datos de "{}" ...'.format(rhost), debug.PER)

            if (wrap.add(md5(bytes_convert.convert(result)).hexdigest(), {'geoip':data}) == True):

                log.logger('¡Almacenado con éxito!', debug.INF)

            else:

                log.logger('Error almacenando los datos de la dirección: "{}"'.format(rhost), debug.COM)

        else:

            log.logger('No se pudo obtener información de "{}". Puede que no sea una dirección válida.'.format(rhost), debug.WAR)
