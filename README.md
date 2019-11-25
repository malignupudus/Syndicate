# Syndicate Project
> Syndicate es un Framework totalmente escrito en Python (**3**) para crear Botnet's, así no es sólo para crear una botnet es para crear cientos o miles, además...

## Caracteristicas

* Cifrado hibrido en las conexiones. Usando AES256 y RSA a nuestro favor podremos cifrar nuestras comunicaciones oficiales entre Evie's, Jacob's y Rook's.
* Cifrado simétrico en las bases de datos, tanto del servidor (**Evie**), como la de los **rook's**. Aunque en los accesos públicos también se usa el mismo esquema.
* Red punto a punto. La red de los Rook's, no es igual a la de los Evie's, aunque puede haber comunicación entre ellas.
* Multi-usuario. El administrador del servidor se encargá de crear tanto usuarios Jacob's cómo Evie's.
* Compartir Rook's entre Evie's
* Comunicación por servidores o lo que quiere decir, que creando una red entre Evie's puedes hacer pasar cada paquete a una dirección o podría decirse nodos intermedios hasta llegar a un punto final o nodo final. La red está diseñada para que no se pueda saber que dirección envío qué y dónde, exceptuando algunas cosas, pero que ya explicaré después y además se tiene que configurar toda la red manualmente; Eso brinda más seguridad.
*

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

* getPubKey: Obtener nuestra clave pública del servidor (**Evie**); Puede tener muchos fines esta operación, pero la más importante es cuando compartirmos un rook y éste requiere de la clave pública a el servidor que lo compartimos.
* saveData: Guarda los datos de perfil del rook
* resend: Re-envía datos a otro nodo, tanto un nodo final como podría ser un nodo intermedio
* sendSOS: Comunicación estilo correo electrónico entre Evie's (Inclusó envío de archivos)

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

Mientras que en Linux:

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



## Creador

~ DtxdF (DtxdF@protonmail.com)

## Agradecimientos

