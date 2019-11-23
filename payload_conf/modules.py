# -*- coding: UTF-8 -*-

# Aquí se cargaran las depencias de los complementos.

import subprocess
import pyperclip
import requests
import os
# Lo que coloco acá, es para que pueda funcionar "pynput".
# Por favor si vas a usar otro SO/Distribución, modificalo o dejalo intacto
if (os.name == 'posix'):
    subprocess.call(['xhost', '+'])
import pynput
import hashlib
import mss
import mss.tools
import pygame
import pyaudio
from utils.Ciphers import generate_uniqkey
from utils.Ciphers import simplycrypt
