#!/bin/bash

declare -a params=($*)

if [ ${#params[@]} -lt 10 ];then

	echo -e 'La longitud de los parámetros no es la acordada.'
	exit 1

fi

for i in $*;do

	if [ "$i" = "-db-help" ];then

		echo "Ejecuto un parámetro erroneo ..."
		exit 1

	fi

done

clear

echo -e "[PID]: $$"

echo -e "\n"

declare -x evie_config="./evie-config.py"
declare -x verify

# Configuration:

declare -A server
declare -A login
declare -A proxy
declare -A honeypot
declare -A style
declare -A templates

# Notas:
#  * True es 1, False es 0. Si dejas una cadena vacia que requiere un tipo de
#    dato booleano, será False.
#  * Hay algunos diccionarios que cierran Evie si no están configurados corr
#    ectamente, tenga cuidado y trate de evitar errores.

# Server:
#  ~ Los valores de este diccionario son especificos para mandar
#    a hacer lo que queramos a Evie (El servidor).
#
#  Claves:
#
#  - lhost          str  : Definimos la dirección IP/Nombre de host para poner en "Escucha" a Evie
#  - lport          int  : El puerto para recibir la conexión
#  - rpath          str  : En el caso de los clientes-administradores (Jacob), se les proporcionará
#                          una ruta para aumentar un poco más la seguridad. Sí se coloca RANDOM (R
#                          espetando Mayúsculas), se genera un URL aleatoria segura
#  - bit_size       int  : El tamaño del par de claves de Evie (El servidor)
#  - sys_version    str  : La versión del Sistema.
#  - server_version str  : La versión del Servidor.
#  - realm          str  : Un pequeño mensaje que se le mostrará al cliente que ingrese al panel
#                          web falso, especificamente la autencicación HTTP básica.
#  - rdns           bool : Resolver en DNS del cliente
#  - rport          bool : Averiguar el servicio utilizado. Ejemplo: 80 (http); Aunque es muy poco
#                          probable que un cliente esté usando un puerto de esa clase
#  - public_server  list : Los servicios públicos permitidos.
#                          En el caso de:
#                          - getPubKey : Permite dejar que los clientes especificos con su respectivo token de
#                                        acceso puedan obtener la clave pública del servidor
#                          - saveData  : Permite guardar los datos de los rook's que alguien desee compartir
#                          - resend    : Permite que Evie se convierta en un nodo de alguna red
#                          - sendSOS   : Permitir recibir mensajes
#  - user_agent    str   : El agente de usuario a utilizar para cuando Evie se convierta en un cliente
#  - nodes_rule          : La regla de cómo debe actuar el orden de los nodos.
#                          - RANDOM    : El algoritmo de shuffle se encargará de "ordenar" de forma aleatoria los
#                                        nodos
#                          - STRICT    : El orden es estricto, por lo tanto así como se guardaron es como viajara
#                                        el paquete
#  - cipher_file   bool  : "True", para cifrar/descifrar los archivos que se envian, "False", lo contrario

server=(
[lhost]='0.0.0.0'
[lport]='8081'
[rpath]='RANDOM'
[bit_size]='2048'
[sys_version]='(Debian)'
[server_version]='Apache/2.4.29'
[realm]='Default: admin:admin123'
[rdns]='1'
[rport]='1'
[public_service]='getPubKey, saveData, resend, sendSOS'
[user_agent]='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
[nodes_rule]='RANDOM'
[cipher_file]='1'
)

# Login:
#  ~ Este diccionario trata controlar las opciones de inicio de sesión en
#    Evie (El servidor)
#
#  Claves:
#
#  - false_username   str  : El nombre de usuario falso para utilizar en el panel de control web falso
#  - false_passphrase str  : La frase de contraseña falsa para utilizar en el panel de control web falso
#  - recover          bool : Sí esto es "True", la penultima clave única se podra usar cómo si fuera
#                            la actual, aunque también se puede usar la actual sin problemas. Esto
#                            representa un riesgo, ya que si pierde la penulta clave única y alguien
#                            tiene sus credenciales podrá acceder sin problemas.
#  - max_retry        int  : Maximo de intentos fallidos antes de bloquear según el método que se
#                            utilice en denied_method
#  - retry_seconds    int  : Maximo de segundos para esperar que una dirección pueda acceder denuebo al sistema
#  - denied_method    str  : El método a usar para la denegación de una entidad
#                            - forIP    : Deniega por dirección IP. Poco inseguro, porque cualquiera podría usar
#                                         proxys por cada intento, pero menos molesto.
#                            - forRetry : Deniega por intentos fallídos según el usuario. Molesto, ya que si
#                                         alguien tiene nuestro nombre de usuario e intenta hacer fuerza bruta,
#                                         no sólo bloquearía esa persona, también a tí.

login=(
[false_username]='admin'
[false_passphrase]='admin123'
[recover]='1'
[max_retry]='5'
[retry_seconds]='80'
[denied_method]='forIP'
)

# Proxy:
#  ~ Acá controlara la lista de proxys (Sí se van usar), para Evie (El servi
#    dor).
#
#  Claves:
#   ~ Este diccionario utiliza "Sumerio" como meta-lenguaje para brindar una
#     sencilla interfaz entre Python y usted (El usuario).
#  - proxy_list Sumerio : Utiliza "Sumerio" como meta-lenguaje para brindar una sencilla interfaz
#                         entre Python y usted (El usuario).
#                         - proxy_type str      : El tipo de proxy a utilizar. Entre ellos están: SOCKS4, SOCKS5 y HTTP
#                         - proxy_addr str      : La dirección del proxy
#                         - proxy_port int      : El puerto del proxy
#                         - rds        bool     : Resolver DNS
#                         - username   str|null : En caso de que el proxy requiera autenticación, aunque si no lo requiere use "null" en su lugar
#                         - password   str|null : Rellenar con una contraseña en la autenticación, aunque si no la requiere use "null" en su lugar
#                         Ejemplo usando tor como proxy: ;a;proxy=list:,dict:;p;proxy_type=str:SOCKS4;p;proxy_addr=str:127.0.0.1;p;proxy_port=int:9050;p;rds=bool:1;p;username=null;p;password=null

proxy=(
[proxy_list]=';a;proxy=list:,dict:;p;proxy_type=str:SOCKS4;p;proxy_addr=str:127.0.0.1;p;proxy_port=int:9050;p;rds=bool:1;p;username=null;p;password=null'
)

# Honeypot:
#  ~ No te dejes engañar por el nombre, tiene como objetivo defender a Evie
#    de un ataque.
#
#  Claves:
#
#  - regular_expression_for_userAgent str : Las expresiones regulares para la detección de los agentes de usuarios
#  - regular_expression_for_address   str : Las expresiones regulares para las direcciones IP's
#  - re_options                       int : Las opciones de las expresiones regulares siguiendo la libraria "re" de
#                                           Python
#  - user_agent_black_list            str : La lista negra de los agentes de usuario
#  - honeypot_list                    str : La lista de direcciones IP's para usar herramientas del sistema. Sintaxis: <Dirección IP>, <Otra Dirección IP>, <¿Otra?>
#  - tools                            str : Las herramientas a ejecutar cuando haya una coincidencia en "honeypot_list".
#                                           tools, tiene una lista de palabras que reconoce y remplaza por un valor especifico:
#                                           - ip      : Usada para indicar la dirección IP coincidente con la lista
#                                                       "honeypot_list". Sintaxis: {ip}
#                                           - port    : 
#                                           - bhost   : Usas la dirección en escucha de Evie (El servidor)
#                                           - bport   : Usas el puerto de Evie (El servidor)
#                                           - phost   : Usar la dirección IP pública de este computador (Requiere de conexión a internet, de lo contrario se usará la local)
#                                           Nota: Si no sigue la siguiente sintaxis "<limite> <programa>  <parámetros>", puede haber un error y no se ejecutara nada
#  - blacklist                        str : La lista negra para las direcciones IP's permitidas. Sigue la misma sintaxis que "honeypot_list"
#
#  Notas:
#
#  * Si usa "!" como primer carácter, significa que si una dirección IP cualquiera no se encuentra en esa lista, se procede a hacer una operación

honeypot=(
[regular_expression_for_userAgent]='0'
[regular_expression_for_address]='0'
[re_options]='2' # Opciones para la búsqueda de patrones; '0', sin opciones.
[user_agent_black_list]='jessssus'
[honeypot_list]='0'
[tools]='2 nmap -T5 -n -r -A --osscan-guess --version-all -Pn -f -vv {ip};1 ping -c 4 {ip}' 
[blacklist]='0' 
)

# Style:
#  ~ Definir el estilo de algunas cosas
#
#  Claves:
#
#  - time str  : El formato a usar para la visualización de la fecha
#  - log  bool : Registrar los mensajes o no en el almacenamiento

style=(
[time]='%H:%M:%S ~ %d/%m/%Y'
[log]='1'
)

# Templates:
#  ~ Ajustar los valores de las plantillas falsas
#
#  Claves:
#
#  - folder          str : La carpeta en donde se encuentran las plantillas
#  - error404        str : La plantilla para el error HTTP 404
#  - error403        str : La plantilla para el error HTTP 403
#  - error511        str : La plantilla para el error HTTP 511
#  - error400        str : La plantilla para el error HTTP 400
#  - error500        str : La plantilla para el error HTTP 500
#  - credentials     str : La plantilla el panel de control web falso
#  - webmaster_email str : La dirección de correo electrónico falso del administrador de la web

templates=(
[folder]='templates'
[error404]='error404/index.html'
[error403]='error403/index.html'
[error511]='error511/index.html'
[error400]='error400/index.html'
[error500]='error500/index.html'
[credentials]='credentials/index.html'
[webmaster_email]='webmaster@gmail.com'
)

CTRL_C_DETECT() {

	echo -e '\033[1;4mCTRL-C\033[0m'
	exit

}

trap CTRL_C_DETECT TERM INT USR1 USR2

if [[ -f "$evie_config" && -x "$evie_config" && -s "$evie_config" ]];then

	./$evie_config -db-check $* > /dev/null
	if [ $? -eq 1 ];then
		echo -e "(1/2) ¡No se pudo pasar la prueba de verificación de errores!"
		exit 1
	fi
	./$evie_config -db-check $* > /dev/null
	if [ $? -eq 1 ];then
		echo -e "(2/2) ¡No se pudo pasar la prueba de verificación de errores!"
		exit 1
	fi

	echo -e "Configurando! ..."

	echo -e "\n"

	echo -e "Configurando: Login:"
	echo -e "\n"

	for key in ${!login[@]};do

		./$evie_config --key "login" --sub-key "$key" --value "${login[$key]}" $*

	done

	echo -e "\n"
	echo -e "Configurando: Server:"
	echo -e "\n"

	for key in ${!server[@]};do

		./$evie_config --key "server" --sub-key "$key" --value "${server[$key]}" $*

	done

	echo -e "\n"
	echo -e "Configurando: Proxy:"
	echo -e "\n"

	for key in ${!proxy[@]};do

		./$evie_config --key "proxy" --sub-key "$key" --value "${proxy[$key]}" $*

	done

	echo -e "\n"
	echo -e "Configurando: Honeypot:"
	echo -e "\n"
	
	for key in ${!honeypot[@]};do

		./$evie_config --key "honeypot" --sub-key "$key" --value "${honeypot[$key]}" $*

	done
	
	echo -e "\n"
	echo -e "Configurando: Style:"
	echo -e "\n"

	for key in ${!style[@]};do

		./$evie_config --key "style" --sub-key "$key" --value "${style[$key]}" $*

	done

	echo -e "\n"
	echo -e "Configurando: templates:"
	echo -e "\n"

	for key in ${!templates[@]};do

		./$evie_config --key "templates" --sub-key "$key" --value "${templates[$key]}" $*

	done

	echo -e "\n"
	echo -e "Configuración exitosa:"

	./$evie_config -print-configuration $*
	echo -e "\n"

	echo -e "Hecho."

	sleep 5

else

	echo -e "[ERROR]: Posibles errores: No existe el script de configuración, no tiene permisos de ejecución o está corrupto el script!"

fi
