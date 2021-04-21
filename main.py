#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
import json
import twitch

sys.dont_write_bytecode = True

import pyaudio
import random

from beep.elements.oscillator import Oscillator
from beep.elements.compressor import Compressor
from beep.elements.sequencer import Sequencer
from beep.constants import SAMPLE_RATE, FRAME_SIZE


def frames_for_seconds(s):
    return int((SAMPLE_RATE * s) / FRAME_SIZE)

def gen_sound(message):
    global pseudo

    # init var
    sender = message.sender
    text = message.text
    bsize = 0.1

    # auto reply
    try:
        if str(sender) != str(pseudo[1]):
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paUInt8,
                            channels=1,
                            rate=SAMPLE_RATE,
                            output=True)

            for lettre in list(text):
                if lettre and lettre != ' ':
                    flt_value = float(str(ord(lettre) * 3) + '.' + str(
                        random.randrange(10, 99)))
                    print(lettre, '>', flt_value)
                    for i in range(0, frames_for_seconds(bsize)):
                        stream.write(Sequencer([flt_value]).gen_frame())
                else:
                    time.sleep(bsize)

            stream.stop_stream()
            stream.close()
            p.terminate()

    except Exception as error:
        print("reply: " + str(error))


if __name__ == '__main__':

    _twitch = os.path.isfile('./.twitch')

    if not _twitch:
        print('twitch_params_error: not .twitch file found')

    with open('./.twitch') as json_file:
        twitch_params = json.load(json_file)

        # TWITCH

        helix = twitch.Helix(twitch_params[0], twitch_params[1])
        OAUTH_KEY = twitch_params[2] # https://twitchapps.com/tmi/
        pseudo = ["TAMA", "anoniji"]

        channel = input('channel: ')
        if channel:
            print("[Twitch] watcher for " + channel)
            chat = twitch.Chat(channel='#'+channel, nickname=pseudo[0], oauth=OAUTH_KEY)
            chat.subscribe(
                lambda message: gen_sound(message)
            )
