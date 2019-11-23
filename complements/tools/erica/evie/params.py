import sys
from utils.UI import evieModule

wrap = evieModule.CreateDatabase('erica')
parser = evieModule.CreateComplement('erica')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: Crack:' + '\n\n'
        '\t' + ' Inicia el crackeo' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'password_hash : str  : El hash a crackear' + '\n'
        '\t\t' + 'wordlist      : list : La lista de contraseñas' + '\n'
        '\t\t' + 'hash_func     : str  : El algoritmo de suma a utilizar'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'Kirari', ['https://github.com/Kirari-Senpai', 'https://underc0de.org/foro/profile/PrudenceSuspect'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')
parser.add(['-show-hashes'], 'show_hashes', 'Mostrar los hashes utilizados', type=bool, action=True)

args = parser.parse_args()

show_hashes = args.show_hashes

if (show_hashes == True):

    hashes = wrap.getall()

    for bot_id, info in hashes.items():

        print('Rook: {}'.format(bot_id))
        print()
        print('    ¿Descifrado?  ~    Hash')
        print()

        for _ in info['hash']:
            
            (key, value) = (_[0], _[1])

            print('         {}       ~    {}'.format('Sí' if (key == True) else 'No', value))

    sys.exit(0)
