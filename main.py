#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
import json
import twitch
import argparse

sys.dont_write_bytecode = True

import pyaudio
import random

from beep.elements.oscillator import Oscillator
from beep.elements.compressor import Compressor
from beep.elements.sequencer import Sequencer
from beep.constants import SAMPLE_RATE, FRAME_SIZE


vibrato = 1.05
rand_min = 10
rand_max = 99
coef = 3
time_bip = 0.1


def frames_for_seconds(s):
    return int((SAMPLE_RATE * s) / FRAME_SIZE)

def gen_sound(message):
    global pseudo
    global vibrato, rand_min, rand_max, coef, time_bip

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
                    flt_value = float(str(ord(lettre) * coef) + '.' + str(
                        random.randrange(rand_min, rand_max)))
                    print(lettre, '>', flt_value)
                    for i in range(0, frames_for_seconds(time_bip)):
                        stream.write(Sequencer([flt_value, flt_value + vibrato, flt_value - vibrato]).gen_frame())
                        time.sleep(time_bip)
                else:
                    time.sleep(time_bip * 2)

            stream.stop_stream()
            stream.close()
            p.terminate()

    except Exception as error:
        print("reply: " + str(error))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--vibrato', type=float, default=vibrato)
    parser.add_argument('--rand_min', type=int, default=rand_min)
    parser.add_argument('--rand_max', type=int, default=rand_max)
    parser.add_argument('--coef', type=int, default=coef)
    parser.add_argument('--time_bip', type=float, default=time_bip)
    args = parser.parse_args()


    vibrato = args.vibrato
    rand_min = args.rand_min
    rand_max = args.rand_max
    coef = args.coef
    time_bip = args.time_bip


    _twitch = os.path.isfile('./.twitch')

    if not _twitch:
        print('twitch_params_error: not .twitch file found')

    with open('./.twitch') as json_file:
        twitch_params = json.load(json_file)

        # TWITCH

        helix = twitch.Helix(twitch_params[0], twitch_params[1])
        OAUTH_KEY = twitch_params[2] # https://twitchapps.com/tmi/
        pseudo = twitch_params[3]

        channel = input('channel: ')
        if channel:
            print("[Twitch] watcher for " + channel)
            chat = twitch.Chat(channel='#'+channel, nickname=pseudo[0], oauth=OAUTH_KEY)
            chat.subscribe(
                lambda message: gen_sound(message)
            )
