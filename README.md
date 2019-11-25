# Syndicate Project
> Syndicate es un Framework totalmente escrito en Python (**3**) para crear Botnet's, así es, no es sólo para crear una botnet es para crear cientos o miles, además...

Tratare de englobar todas las caracteristicas posibles de Syndicate, espero no me falté nada :)...

## Caracteristicas

* Cifrado hibrido en las conexiones. Usando AES256 y RSA a nuestro favor podremos cifrar nuestras comunicaciones oficiales entre Evie's, Jacob's y Rook's.
* Cifrado simétrico en las bases de datos, tanto del servidor (**Evie**), como la de los **rook's**. Aunque en los accesos públicos también se usa el mismo esquema.
* Red punto a punto. La red de los Rook's, no es igual a la de los Evie's, aunque puede haber comunicación entre ellas.
* Multi-usuario. El administrador del servidor se encargá de crear tanto usuarios Jacob's cómo Evie's.
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

**Pero** antes de hacer éso, quiero aclarar que algunas herramientas necesitan acceso seguro a la base de datos que está encriptada, por lo tanto si usted no introducé los parámetros se le va abrir un pequeño formulario requiriendo los datos. Sí no me cree, mirelo usted o mejor aún **Pruébelo**:

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

¿Ven?, sería tedíoso que tuviera que introducir todo esas cosas, mejor usas nuestra linda terminal :'D:

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

## Complementos

## Plataformas

* Lamentablemente sólo la probé en Kali linux, pero puede experimentar en otras plataformas.
* Recomiendo que si usted va a probar Syndicate en Windows, use Cygwin o WSL, aunque no le garantizó nada.

## Requerimientos

Puede optar por una fácil instalación con PIP, pero hay algunos inconvenientes que dependen de usted.

* En primer lugar, lo que si es necesario ejecutar es [requirements/requiremnts.txt](https://github.com/DtxdF/Syndicate/tree/master/requirements):

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

Un último requerimiento más para los complementos predeterminados sería "PyAudio", pero esto requiere un poco más de tu colaboración:

En el caso de **Windows**:

Seleccione la versión correspondiente: [PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

En mi caso es: PyAudio‑0.2.11‑cp37‑cp37m‑win32.whl

Mientras que en **Linux**:

sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg
sudo pip install PyAudio==0.2.11

Usted se estará preguntado: *¿Windows?, ya mencionaste que sólo funciona en **Linux***, Claro, esto solo requerimientos son para los complementos dependiendo del SO a atacar.

## Creando mi propio payload

## Instalación

```
git clone https://github.com/DtxdF/Syndicate
cd Syndicate
```

## Limitaciones

## Capturas de pantalla:



## Creador

~ DtxdF (DtxdF@protonmail.com)

## Agradecimientos

