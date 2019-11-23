import sys
from json import dumps
from utils.UI import evieModule

wrap = evieModule.CreateDatabase('symplix')

parser = evieModule.CreateComplement('symplix')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: tree:' + '\n\n'
        '\t' + ' Lista todos los archivos posibles.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'path      : str        : El directorio a usar' + '\n\n'
        '\t' + 'Función: encrypt:' + '\n\n'
        '\t\t' + ' Encripta un archivo.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'file      : str        : La ruta del archivo a encriptar' + '\n'
        '\t\t' + 'extension : str        : La extensión a usar cuando finalize el proceso' + '\n\n'
        '\t' + 'Función: decrypt:' + '\n\n'
        '\t' + ' Desencripta un archivo.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'file      : str        : La ruta del archivo a desencriptar' + '\n'
        '\t\t' + 'key       : str        : La contraseña para desencriptar' + '\n'
        '\t\t' + 'extension : str        : La extensión perteneciente' + '\n'
        '\t\t' + 'exception : bool:False : Mostrar la excepción verdadera' + '\n\n'
        '\t' + 'Función: tree_encrypt:' + '\n\n'
        '\t' + ' Encripta todos los archivos posibles.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'directory : str        : La ruta de los archivos a encriptar' + '\n'
        '\t\t' + 'extension : str        : La extensión a usar cuando finalice el proceso' + '\n\n'
        '\t' + 'Función: tree_decrypt:' + '\n\n'
        '\t' + ' Desencripta todos los archivos posibles.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'data      : list       : Una lista con todos los datos generados por "encrypt"' + '\n'
        '\t\t' + 'extension : str        : La extensión perteneciente'
        )

parser.set_requirements('pycryptodome', '3.9.0', '>=')
parser.set_requirements('secrets')

parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')
parser.add(['-show-password'], 'show_password', 'Mostrar las contraseñas de descifrado', type=bool, action=True)

args = parser.parse_args()

show_password = args.show_password

if (show_password == True):

    print(dumps(wrap.getall(), indent=6))
    
    sys.exit(0)
