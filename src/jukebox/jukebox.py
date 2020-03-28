#!/usr/bin/env python3


import argparse
import logging
import subprocess
import datetime
import vlc
import time

from evdev import InputDevice, categorize, ecodes

from db import read_jbdb

class JukeBox(object):

    MIN_TIME_BETWEEN_SWIPES_IN_SEC = 10

    def __init__(self, device_path: str, db_path: str):
        """
        :param device_path:
        :param db_path:
        """

        self._device_path = device_path
        self._db_path = db_path
        self._logger = logging.Logger(name="JukeBox Logger")
        self._logger.setLevel(logging.INFO)
        self._vlcInstance = vlc.Instance()
        self._vlc_player = self._vlcInstance.media_player_new()
        self._last_user_action = None

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
                        self._logger.error('Failed trigger action')
                        self._logger.error(e)
                    finally:
                        chip_swiped = False
                        trigger_action = False
                        event_strings = []

    def _vlc_play(self, sound_file_path: str) -> None:
        """
        :param sound_file_path:
        """

        msg = 'Playing {}'.format(sound_file_path)
        self._logger.warning(msg)

        self._vlc_player.set_mrl(sound_file_path)
        self._vlc_player.play()


    def play_file(self, sound_file_path: str) -> None:
        """
        :param sound_file_path:
        """

        if self._vlc_player.is_playing() and not self._check_rfid_swipe_is_valid():
            logging.warning('RFID swipe too quick')
            return

        self._last_user_action = datetime.datetime.now()

        self._logger.warning(msg)

        self.LAST_USER_ACTION = datetime.datetime.now()

        self._vlc_play(sound_file_path)
        time.sleep(0.1)

    def play_playlist(self, sound_files: str):
        """
        Plays a list of sound files
        :param sound_files: list of files
        """

        for sound_file in sound_files:
            self.play_file(sound_file)

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

            logging.warning("Recieved code {} - {}".format(code, sound_file_path))

            if type(sound_file_path) == list:
                self.play_playlist(sound_file_path)
            elif type(sound_file_path) == str:
                self.play_file(sound_file_path)

    def _check_rfid_swipe_is_valid(self):
        """
        Determines whether time at call is outside of miminum swipe time interval
        """

        now = datetime.datetime.now()
        difference = now - self._last_user_action

        return difference.total_seconds() > self.MIN_TIME_BETWEEN_SWIPES_IN_SEC

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