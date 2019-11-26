# Syndicate Project
> Syndicate es un Framework totalmente escrito en Python (**3**) para crear Botnet's, así es, no es sólo para crear una botnet es para crear cientos o miles, además...

Tratare de englobar todas las caracteristicas posibles de Syndicate, espero no me falté nada :)...

## Caracteristicas

* Cifrado hibrido en las conexiones. Usando AES256 y RSA a nuestro favor podremos cifrar nuestras comunicaciones oficiales entre Evie's, Jacob's y Rook's.
* Cifrado simétrico en las bases de datos, tanto del servidor (**Evie**), como la de los **rook's**. Aunque en los accesos públicos también se usa el mismo esquema.
* Red punto a punto. La red de los Rook's, no es igual a la de los Evie's, aunque puede haber comunicación entre ellas.
* Multi-usuario. El administrador del servidor se encargá de crear tanto usuarios Jacob's cómo Rook's con sus respectivos privilegios
* Compartir Rook's entre Evie's
* Comunicación por servidores o lo que quiere decir, que creando una red entre Evie's puedes hacer pasar cada paquete a una dirección o podría decirse nodos intermedios hasta llegar a un punto final o nodo final. La red está diseñada para que no se pueda saber que dirección envío qué y dónde, exceptuando algunas cosas, pero que ya explicaré después y además se tiene que configurar toda la red manualmente; Eso brinda más seguridad.
* Uso de proxy's para mayor privacidad.
* Sistema antí fuerza bruta: Esto es relativo. Relativo según las configuraciones que ejerce el administrador y el mismo usuario. porque el administrdor decide cómo **Evie**, va a bloquear a un usuario, cuándo y porqué. Dejaré la explicación más adelante.

### Tipos de configuración

Existen dos tipos de configuración para que el funcionamiento de Syndicate sea satisfactorio, también sus razones de esta división:

* Configuración Dinámica: Este tipo de configuración puede cambiar en plena ejecución de *Evie.py* dependiendo de lo que haga el administrador del servidor
* Configuración Estatica: También se puede llamar configuración global, porque se en la mayoria de herramientas, utilidades, entre otras cosas de Syndicate

### Tipos de usuario

En syndicate project trato de implementar diferencias entre usuarios para simplificar las explicaciones; En el susodicho proyecto se puede encontrar cuatro tipos de usuario:

* **Administrador del servidor**: El administrador del servidor, se encargá de controlar **todo** lo relacionado con el servidor interno, base de datos, seguridad, usuarios, configuración o basicámente todo lo que se pueda hacer en una computadora o VPS con Linux.

* **Jacob**: Él es el cliente-administrador de los *rooks*. Jacob podrá controlar tantos *rooks* cómo el *Administrador del servidor* desee.
* **Rook**: El cliente-bot que se encarga de hacer lo que le pida **Jacob**
* **Public**: Yo no diría que es un usuario en sí, se podría decir que es un cliente que quiere usar nuestros servicios públicos cómo:

  - getPubKey: Obtener nuestra clave pública del servidor (**Evie**); Puede tener muchos fines esta operación, pero la más importante es cuando compartirmos un rook y éste requiere de la clave pública a el servidor que lo compartimos.
  - saveData: Guarda los datos de perfil del rook
  - resend: Re-envía datos a otro nodo, tanto un nodo final como podría ser un nodo intermedio
  - sendSOS: Comunicación estilo correo electrónico entre Evie's (Inclusó envío de archivos)

## Aclaraciones

Tengo que explicar algunas cosas, para que no haya perdidas de tiempo:

* **Redirector**: Es un **Rook** que pasa hacer un **servidor** (No un **Evie**) dentro de la máquina infectada; consiste en crear un servidor capaz de recibir datos, almacenarlos en una base de datos cifrada dentro de la misma máquina victima, para que luego el administrador del servidor, pueda conectarse, descargar los datos y simular ser **Evie**, con el único fín de obtener un resultado y enviarselo a un rook de forma transparante o como si no fuera sucedido nada.

El redirector es mejor usarlo, cuando deseas crear un "Backup" dentro de las máquinas infectadas *¿Por qué?*, ¿Te imaginas que tu servidor central callerá? y luego cuando lo vuelvas a lenvantar ya es muy tardé, no tienes como recuperar la perdida de datos; hay es cuando entra redirector al rescate.

* **Hash dinámico**: En syndicate se usa un **Hash dinámico**, para hacer todo lo posble para evitar un ataque de fuerza bruta o por diccionario, usando *iteraciones*, *Número de seguridad*, *Número de disminución* y *Caracteres de seguridad*; todo esto tiene que ver con el algoritmo utilizado, pero haciendo una aclaratoria:

  - **Iteraciones**: Las iteraciones son el número de veces por que se repité el proceso
  - **Número de seguridad**: El número de seguridad se multiplica primero por el mismo y el resultado se usa para delimitar la ofuscación de caracteres de seguridad y luego en la siguiente iteración (**Si es que la hay**) disminuye usando el número de disminución
  - **Número de disminución**: El número de disminución se encarga de disminuir el número de seguridad por cada segunda iteración
  - **Caracteres se seguridad**: Los caracteres de seguridad se codifican a base64 y se "parten" y ofuscan usando el número de seguridad y disminución, para luego sumarlos con el resultado verdadero, que quiere decir, el hash.
  
  **Nota**: *El hash usa la siguiente función: sha256( sha512( string ).digest() ).hexdigest()*
  
  - **Token de Acceso**: Usado para verificar que tenga acceso público al sistema y cifrar los datos, posteriormente se usaría algún servicio antes mencionado.
  
  - **Clave secreta**:  La clave secreta cifra algunos datos antes de usar "resend" o un reenvio de paquetes en una red, porque que si llega a hacer interceptada, no se pueda "leer" esos datos, por eso su nombre, ésta sólo se debe compartir con las personas de confianza, igual que pasa con el *token de acceso*.

**Notas**:

* Tú, como administrador del servidor te debes encargar de repartir a personas de confianza el token de acceso, claro sí es qué desean usar los servicios públicos.
* El token de acceso se tiene que usar mayormente para usar **Compatir un rook** o usar **resend**.
* En el caso de usar **resend**, debe usar igualmente el token de acceso
* Prefiero que usted use [sendSOS](sendSOS.py) y se comuniqué con el **Evie** que desee, para que tenga más seguridad en sus datos y sin limitaciones por parte de servidores externos. Aclaró ésto, porque así es la mejor manera de enviar token's de acceso y/o claves secretas.
* Tengo absoluto cuidado con los números y caracteres de seguridad, pueden volver el proceso más lento, pero eso no es tan malo, porque si un atacante quiere hacer fuerza bruta, tiene que esperar a que el servidor genere el hash y luego verificar si es correcto o no. ¿Una maravilla no? :')
* Sí quieres saber más acerca del algoritmo, puedes hacerlo [Aquí](modules/Ciphers/db_hash.py)

## Funcionamiento de la Red

Algunas veces es mejor dejar una simulación en vez de palabras, por lo tanto [Aquí](https://onodo.org/visualizations/98665), podrá encontrar el cómo sería la red con todas las caracteristicas.

Ahora pasemos a la explicación: Es sencilla la red, hay que saber usarla y cuándo, pero para poder entenderla hay que crear desde un principio lo que necesitamos e ir aumentando.

Primero crearemos un **Jacob** (Administrador de los Rook's):

**Pero** antes de hacer éso, quiero aclarar que algunas herramientas necesitan acceso seguro a la base de datos que está encriptada, por lo tanto si usted no introducé los parámetros se le va abrir un pequeño formulario requiriendo los datos. Sí no me cree, mirelo usted o mejor aún [Pruebélo](modules/Ciphers/db_hash.py):

```bash
./addadmin.py -u <Nombre de usuario> -p <Frase de contraseña> -P <Frase de contraseña de la clave privada>
* Datos para desencriptar la frase de contraseña *
  ----------------------------------------------

Ingrese la frase de contraseña:
: **************
Ingrese los caracteres de seguridad:
: abcdefghijklmnopqrstuvwxyz1234567890
Ingrese el número de iteraciones:
: 43
Ingrese el número de seguridad:
: 30
Ingrese el número de disminución:
: 18
Se guardo satisfactoriamente en -> conf/pass
```

**Notas**:

* Los que acabo de introducir se genera lento en mi computadora, usted tiene que introducir lo necesario para obtener una mayor seguridad pero que el proceso no se vuelva tan lento; al fin y al cabo usted decide.
* Sí ejecutan alguna herramienta que requiera la información para desencriptar la base de datos, se guardará en vez de comparar
* **conf/pass** es guardado con permisos "**444**", por favor verifique que sea así con "ls -l conf/pass" o si no hagalo de forma manual: chmod 444 conf/pass una vez ha sido creada.

¿Ven?, sería tedíoso que tuviera que introducir todo esas cosas, mejor usamos nuestra linda terminal :'D:

```bash
# Primero veamos que regla para guardar los comando en el historial tenemos
echo $HISTCONTROL
ignoreboth
# ¡Bien!, esa es la regla perfecta.
# Eso nos servirá cuando introduscamos un comando y no se guarde en el historial, ya que la idea es que no se guarde una contraseña o algo sensible.
# Así que ahora guardemos lo que necesitamos en una variable
 declare -x params='-db-passphrase <Frase de contraseña de la base de datos> -db-iterations <Número de iteraciones> -db-chars <Caracteres de seguridad> -db-security-number <Número de seguridad>'
# Cómo pueden notar, usé un espacio antes de escribir el comando, para que no se almacene en el historial.
# Claro, pueden hacer éso o pueden crear un script y lo cargán usando "source" o ".", pero se los dejo para la casa...
```

Ahora simplemente puede ejecutar:

```bash
./addadmin.py -u <Nombre de usuario> -p <Frase de contraseña> -P <Frase de contraseña de la clave privada> $params
```

Al ejecutar se dará cuenta que le pide una confirmación:

```
-*- ¿Es correcta la siguiente información? -*-

Nombre de usuario       ::   <Nombre de usuario>
Frase de contraseña     ::   <Frase de contraseña>
Contraseña RSA          ::   <Frase de contraseña de la clave privada>
Iteraciones             ::   43
Número de seguridad     ::   30
Número de disminución   ::   18
Caracteres de seguridad ::   abcdefghijklmnopqrstuvwxyz1234567890
Privilegios             ::   ALL
Max. de bot's           ::   0 (infinito)
Tamaño de la clave      ::   2048
¿Root?                  ::   0
->
```
Debe introducir "**1**" para continuar y "**0**" para salir, aunque "**CTRL-C**", también ayuda.

**Notas**:

* Sí no quiere que le confirme los datos, usé "-no-confirm".
* Cómo puede observar, hay caracteres rellenados automáticamente, puede editarlos introduciendo los parámetros correspondientes cómo: "**-i, --iterations**" para las *Iteraciones* "**-sn, --security-number**" para el "*número de seguridad*", "**-c, --security-chars**" para los *Caracteres de seguridad* y "**-d, --decrement-number**" para el *Número de disminución* o puede editarlos en el [archivo de configuración global](conf/global_conf.py).
* Ser **root** no es lo mismo en **Linux** que en **syndicate**, **no se confunda**; significa que todos los **rook's** ahora pertenecerán a todos los **jacob's**, aunque esto es relativo, ya que si el **maximo de bot's** es mayor a "**0**" no se incluirá si llegó a su maximo.

Esperamos unos instantes y para confirmar que todo salío perfecto, ejecuté:

```bash
./addadmin.py -show $params
```
Ese comando le mostrará todos los **Jacob's** registrados.

Ahora pasemos a algo mejor, creemos nuestro **rook** para un **jacob**:

```bash
./addbot.py -u <Nombre del rook> -p <Frase de contraseña> -P <Frase de contraseña de la clave privada> -a <Administrador> $params
```

Vemos un parámetro nuevo, "**-a**" o también podría llamarse "**--admin**". Si no razonaste correctamente, te digo que es para agregar a los **Jacob's**.

**Notas**:

* Puedes crear tantos **rook's** para **jacob's** dependiendo del **maximo de bot's**
* El parámetro "**-a, --admin**" es de tipo **lista**, lo que quiere decir que para agregar a más de uno, tienes que usar una "**,**" (**coma**) y sí el nombre tiene espacios usa comíllas cómo apoyo.

Eso no es todo, necesitamos configurar [Evie](evie.py) usando [auto-config.sh](auto-config.sh) mas los parámetros ya utilizados en anteriores herramientas.

```bash
./auto-config.sh $params
```
Usted vería cada **Clave**, **Sub-Clave** y **Valor**; los segundos que se muestran cada uno, varian dependiendo de sus recursos, esto se debe a que se está encriptado cada dato.

A pesar de que se muestre la configuración al finalizar, tal vez usted quiera apreciarla para un después. Lo puede hacer así:

```bash
./evie-config.py -print-configuration $params
```

**Notas**:

* Aunque [auto-config.sh](auto-config.sh) es un script, la herramienta que tiene el poder de hacer esta mágia es [evie-config.py](evie-config.py), pero es mejor automatizar todo, para ahorrar tiempo.
* Puede obtener más información desde el mismo [Archivo de Configuración](auto-config.sh).

Ahora si que viene lo bueno, ejecutamos [evie.py](evie.py) para iniciar el servidor:

```bash
./evie.py -P <Frase de contraseña de la clave privada> $params
```

La salida sería algo así:

```
(00:33:04 ~ 26/11/2019)[Evie:ADVERTENCIA]:---:!: El par de claves aún no son son generados ... generando ...
(00:33:04 ~ 26/11/2019)[Evie:PERSONAL]:------:+: Tamaño a generar: "2048"
(00:33:11 ~ 26/11/2019)[Evie:INFORME]:-------:*: El par de claves fueron generadas ...
(00:33:11 ~ 26/11/2019)[Evie:INFORME]:-------:*: Desencriptando ...
(00:33:12 ~ 26/11/2019)[Evie:INFORME]:-------:*: ¡Clave desencriptada!
(00:33:12 ~ 26/11/2019)[Evie:INFORME]:-------:*: Generando clave secreta ...
(00:33:12 ~ 26/11/2019)[Evie:PERSONAL]:------:+: Clave secreta generada -> b22f 34b4 1c48 b8dd dad3 dcfc d0b6 986d 081f 80f3 959d 3de0 1075 6ea1 dfc2 ad45
(00:33:12 ~ 26/11/2019)[Evie:INFORME]:-------:*: Generando un nuevo token de acceso ...
(00:33:12 ~ 26/11/2019)[Evie:PERSONAL]:------:+: Token de acceso generado -> 8502382584368ce06c336c793750815f400697daaff7dc8244e849b75135d638
(00:33:12 ~ 26/11/2019)[Evie:ADVERTENCIA]:---:!: No se encontraron los requerimientos necesarios para usar el protocolo de forma (más) segura. Usando HTTP ...
(00:33:12 ~ 26/11/2019)[Evie:PERSONAL]:------:+: Escuchando en :: http://0.0.0.0:8081/hmKReYEJrMWB8l48yvsENaLlMT1ijqIiU2nU6RGiKnanCZEkimT0lh2xW-xS1xYP6rJX1uWmxbp2bOeSVCCfJQ
```

No explicaré todo, porque hay cosas que son sencillas y otras ya las explique, pero sí que hay algo nuevo. *¿Qué deminios es esa ruta?*; la ruta se genera de forma aleatoria y segura, puede usar los archivos de configuración para evitarlo, pero recomiendo que lo deje así.

Lo negativo de usar una ruta aleatoria es que si el servidor se "apaga" y se inicia nuevamente, tendrá otra ruta, lo que quiere decir que los **Jacob's** tendran que saberlo; es recomendable sólo cuando hay pocos **Jacob's**.

**Nota**: Puede usar el parámetro "**-h, --help**" para ver la ayuda en la mayoría de herramientas.

## Complementos

## Plataformas

* Lamentablemente sólo la probé en Kali linux, pero puede experimentar en otras plataformas.
* Recomiendo que si usted va a probar Syndicate en Windows, use Cygwin o WSL, aunque no le garantizó nada.
* En Android tecnicamente debería funcionar con Userland, aunque tmux no es mala elección.

## Requerimientos

Puede optar por una fácil instalación con PIP, pero hay algunos inconvenientes que dependen de usted.

* En primer lugar, lo que si es necesario ejecutar es [requirements/requiremnts.txt](requirements/requirements.txt):

python3 -m pip install -r requirements/requirements.txt

```
PySocks==1.7.1
pycryptodome==3.9.4
PyYAML==5.1.2
pager==3.3
requests==2.22.0
urllib3==1.25.7
certifi==2019.9.11
chardet==3.0.4
idna==2.8
pyperclip==1.7.0
```

Estos son los requerimientos para que funcione lo más principal de Syndicate, mientras que para los complementos se tendría que seguir los siguientes pasos, no obstante no es necesario instalar para las funcionalidades anteriormente mencionadas, esto sirve para aumentar el poder...

```
requests==2.22.0
pynput==1.4.5
six==1.13.0
python-xlib==0.25
pygame==1.9.6
mss==4.0.3
```

Un último requerimiento para los complementos predeterminados sería "PyAudio", pero esto requiere un poco más de su colaboración:

En el caso de **Windows**:

Seleccioné la versión correspondiente: [PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

En mi caso es: PyAudio‑0.2.11‑cp37‑cp37m‑win32.whl

Mientras que en **Linux**:

```bash
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg
sudo pip install PyAudio==0.2.11
```

Usted se estará preguntado: *¿Windows?, ya mencionaste que sólo funciona en **Linux***, Claro, estos requerimientos son para los complementos dependiendo del SO a atacar.

## Instalación

```
git clone https://github.com/DtxdF/Syndicate
cd Syndicate
```

## Limitaciones

## Capturas de pantalla

### Inicio de sesión para Jacob

![](shots/login.Syndicate.png)
![](shots/TUI.Syndicate.png)

### Compartiendo un Rook

![](shots/Compartiendo_un_rook.Syndicate.png)

### Comunicación de un Rook con varios servidores

![](shots/Rook_ejecutando_varias_operaciones_en_varios_servidores.Syndicate.png)

### Nodos

![](shots/nodos.Syndicate.png)

## Creador

~ *Jesús D. Colmenares* - DtxdF (**DtxdF@protonmail.com**)

## Agradecimientos

