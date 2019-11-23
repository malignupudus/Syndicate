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

# True es 1, False es 0

server=(
[lhost]='0.0.0.0'
[lport]='8081'
[rpath]='RANDOM'
[bit_size]='2048'
[sys_version]='(Debian)'
[server_version]='Apache/2.4.29'
[realm]='Members only'
[rdns]='1'
[rport]='1'
[public_service]='getPubKey, saveData, resend, sendSOS'
[user_agent]='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
[nodes_rule]='RANDOM' # or STRICT
[cipher_file]='1'
)

login=(
[false_username]='admin'
[false_passphrase]='admin123'
[recover]='1'
[max_retry]='5'
[retry_seconds]='80'
[denied_method]='forIP' # forIP or forRetry
)

proxy=(
[proxy_type]='SOCKS4'
[proxy_addr]='127.0.0.1:9050'
[rds]='1'
[username]='None'
[password]='None'
)

honeypot=(
[regular_expression_for_userAgent]='0'
[regular_expression_for_address]='0'
[re_options]='2' # Opciones para la búsqueda de patrones; '0', sin opciones.
[user_agent_black_list]='0'
[honeypot_list]='0' # Formato: [backlist]='<hostname_ip>#<port>', si colocas '0' como puerto sélo se usara la dirección IP/Nombre de host; Sí esta en 0, no se usan las herramientas.
[blacklist]='0'
[tools]='1{limit}nmap{program} -T5 -n -r -A --osscan-guess --version-all -Pn -f -vv {ip}' # A pesar que el formato lo tengas que definir '<ip>:<port>' obligatoriamente, en las herramientas puedes usarlos como te plazca.
)

style=(
[time]='%H:%M:%S ~ %d/%m/%Y'
[log]='1'
)

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

trap CTRL_C_DETECT TERM INT

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
