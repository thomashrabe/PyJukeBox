#!/usr/bin/env python3


import argparse
import logging
import subprocess
import datetime


from evdev import InputDevice, categorize, ecodes


from db import read_jbdb


class JukeBoxState(object):
    """
    Stores a the jukebox state
    """

    CURRENTLY_PLAYING = False
    CURRENT_AUDIO_FILE = None
    LAST_USER_ACTION = None
    MIN_TIME_BETWEEN_SWIPES_IN_SEC = 10

class JukeBox(JukeBoxState):

    def __init__(self, device_path: str, db_path: str):
        """
        :param device_path:
        :param db_path:
        """

        self._device_path = device_path
        self._db_path = db_path

    def start(self):
        """
        Just a proxy function for calling
        """
        self.rfid_input_loop()

    def rfid_input_loop(self):
        """
        Read RFID reader input in a loop, trigger actions when 
        a card was read.
        """

        device = InputDevice(self._device_path)

        chip_swiped = False
        trigger_action = False
        event_strings = []

        # This is an infinite loop
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:

                event_string = str(categorize(event))

                event_strings.append(event_string)

                if not chip_swiped and '11 (KEY_0), down' in event_string:
                    chip_swiped = True

                if chip_swiped and '28 (KEY_ENTER), up' in event_string:
                    chip_swiped = False
                    trigger_action = True

                if trigger_action:
                    try:
                        self.on_user_card_swipe(event_strings)
                    except Exception as e:
                        logging.error('Failed trigger action')
                        logging.error(e)
                    finally:
                        chip_swiped = False
                        trigger_action = False
                        event_strings = []


    def play_file(self, sound_file_path):
        """
        :param sound_file_path:
        """
        pass

    def convert_event_strings_to_code(self, event_strings: [str]) -> str:
        """
        Converts a list of RFID readings to a card specific code
        :param event_strings:
        """
        code = ''
        for event_string in event_strings:

            if 'KEY_0' in event_string or 'KEY_ENTER' in event_string:
                continue
            
            suffix = event_string.split('KEY_')[1]
            v = suffix.split(')')[0]

            code += v
        
        return code

    def on_user_card_swipe(self, event_strings: [str]):
        """
        Responds to user card swipe and 
        :param event_strings:
        """

        code = self.convert_event_strings_to_code(event_strings)

        jbdb = read_jbdb(self._db_path)

        sound_file_path = jbdb.get(code)
        
        if sound_file_path is not None:

            print(code, sound_file_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='JukeBox.')
    parser.add_argument('--db',
                        type=str,
                        help='Path to RFID - MP3 library',
                        required=True)

    parser.add_argument('-i',
                        type=str,
                        help='Device path to RFID reader',
                        default='/dev/input/event0')

    parser.add_argument('-t', action='store_true',
                        help='Test mode')

    args = parser.parse_args()

    jukebox = JukeBox(args.i, args.db)

    jukebox.start()