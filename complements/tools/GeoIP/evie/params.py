import sys
from utils.UI import evieModule
from json import dumps

wrap = evieModule.CreateDatabase('GeoIP')

parser = evieModule.CreateComplement('GeoIP')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: geolocation:' + '\n\n'
        '\t' + ' Obtiene la dirección IP pública' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'No requiere parámetros'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')
parser.add(['-show'], 'show', 'Muestra las direcciones IP\'s guardadas con su geolocalización', type=bool, action=True)
parser.add(['-format'], 'format', 'El formato a usar. [JSON o RAW]', uniqval=['json', 'raw'], default='raw')

args = parser.parse_args()

show = args.show
format_ = args.format

if (show == True):

    if (format_ == 'json'):

        print(dumps(wrap.getall(), indent=6))

    elif (format_ == 'raw'):

        for key, value in wrap.getall().items():

            data = value['geoip']

            print('\033[1;4;33mID:\033[0m \033[1;4;37m{}\033[0m'.format(key))
            print()
            
            if (data.get('status') == 'success'):

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

            else:

                print('\033[1;33m¡No se obtuvo datos de {}!\033[0m'.format(data.get('query')))

            print()

    else:

        pass

    sys.exit(1)
