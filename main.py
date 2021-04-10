import sys
sys.dont_write_bytecode = True

import pyaudio
import random

from beep.elements.oscillator import Oscillator
from beep.elements.compressor import Compressor
from beep.elements.sequencer import Sequencer
from beep.constants import SAMPLE_RATE, FRAME_SIZE


def frames_for_seconds(s):
    return int((SAMPLE_RATE * s) / FRAME_SIZE)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paUInt8,
                channels=1,
                rate=SAMPLE_RATE,
                output=True)

while True:
    word = input('word: ')
    for lettre in list(word):
        if lettre and lettre != ' ':
            flt_value = float(str(ord(lettre) * 3) + '.' + str(random.randrange(10, 99)))
            print(flt_value)
            for i in range(0, frames_for_seconds(1)):
                stream.write(Sequencer([flt_value]).gen_frame())

stream.stop_stream()
stream.close()
p.terminate()
