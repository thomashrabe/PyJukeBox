#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import datetime
import vlc
import time

from evdev import InputDevice, categorize, ecodes

import db

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
        self._playlist = None

    def start(self):
        """
        Just a proxy function for calling
        """

        print('-----------------------------------')
        print('|                                 |')
        print('|             JukeBox             |')
        print('|                                 |')
        print('-----------------------------------')
        print('|                                 |')
        print('|       Start swiping your        |')
        print('|       RFID Cards to play        |')
        print('|       your favorite tracks      |')
        print('-----------------------------------')

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

        # Run process loop forever
        while True:
            try:
                # read will raise BlockingIOError if no RFID chip 
                # is read
                for event in device.read():
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
            except BlockingIOError:
                pass

            if not self._vlc_player.is_playing() and self._playlist is not None:
                self.play_playlist(play_confirmation=False)

            time.sleep(0.1)

    def _vlc_play(self, sound_file_path: str) -> None:
        """
        :param sound_file_path:
        """

        msg = 'Playing {}'.format(sound_file_path)
        self._logger.warning(msg)

        self._vlc_player.set_mrl(sound_file_path)
        self._vlc_player.play()


    def play_file(self,
                  sound_file_path: str,
                  play_confirmation: bool=False) -> None:
        """
        :param sound_file_path:
        :param play_confirmation: Whether to play confirmation sound or not
        """

        if self._vlc_player.is_playing() and not self._check_rfid_swipe_is_valid():
            logging.warning('RFID swipe too quick')
            return
        if play_confirmation:
            self.play_confirmation_sound()

        self._last_user_action = datetime.datetime.now()

        self._vlc_play(sound_file_path)
        time.sleep(0.1)

    def play_playlist(self, play_confirmation: bool=False) -> None:
        """
        Plays a list of sound files, skips to next song
        if same playlist is selected repeatedly
        :param play_confirmation: Whether to play confirmation sound or not
        """

        if len(self._playlist) > 0:

            sound_file = None
            if self._vlc_player.is_playing():
                # skip to song after current song same playlist 
                # was selected again
                current_media = self._vlc_player.get_media()
                current_mrl = current_media.get_mrl().replace('file://', '')

                # compare if current track is in playlist
                if current_mrl in self._playlist:
                    index = self._playlist.index(current_mrl)
                    if index < len(self._playlist) - 1:
                        # If there's at least one more track after the current
                        # play the next song
                        sound_file = self._playlist.pop(index + 1)
                    else:
                        # Do nothing
                        return
                else:
                    # Play first song of new playlist
                    sound_file = self._playlist.pop(0)
            else:
                # Start with the first song if is currenly not playing
                sound_file = self._playlist.pop(0)

            self.play_file(sound_file,
                           play_confirmation=play_confirmation)

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

        sound_file_path = db.lookup_item_for_rfid_code(code, self._db_path)

        if sound_file_path is not None:

            logging.warning("Recieved code {} - {}".format(code, sound_file_path))

            if sound_file_path == 'STOP':
                self.stop()
                self.play_confirmation_sound()
            else:

                if type(sound_file_path) == list:
                    self._playlist = sound_file_path
                    self.play_playlist(play_confirmation=True)
                elif type(sound_file_path) == str:
                    self.play_file(sound_file_path,
                                   play_confirmation=True)

    def play_confirmation_sound(self):
        """
        Plays confirmation sound on card swipe before playing an item
        """
        confirmation_sound_path = db.get_confirmation_sound_path(self._db_path)
        self._vlc_play(confirmation_sound_path)
        time.sleep(2)

    def _check_rfid_swipe_is_valid(self):
        """
        Determines whether time at call is outside of miminum swipe time interval
        """

        now = datetime.datetime.now()
        difference = now - self._last_user_action

        return difference.total_seconds() > self.MIN_TIME_BETWEEN_SWIPES_IN_SEC

    def add_new_mp3(self, sound_file_path: str) -> None:
        """
        :param sound_file_path:
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

                        self._add_new_sound_file(event_strings, sound_file_path)
                        self._logger.warning('{} added to JukeBox DB {}'.format(
                            sound_file_path, self._db_path))
                        self.play_confirmation_sound()
                    except Exception as e:
                        self._logger.error('Failed adding new sound file')
                        self._logger.error(e)
                    finally:
                        break

    def _add_new_sound_file(self, event_strings: [str], sound_file_path: str) -> None:
        """
        :param event_strings:
        :param sound_file_path:
        """

        code = self.convert_event_strings_to_code(event_strings)
        logging.warning('Adding new code {} and file {}'.format(code, sound_file_path))
        db.add_new_file(self._db_path, code, sound_file_path)


    def stop(self):
        """
        Stop jukebox
        """

        if self._vlc_player.is_playing():
            self._playlist = None
            self._vlc_player.stop()


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

    parser.add_argument('-a',
                        type=str,
                        help='Add new mp3 to library. Specify mp3 path, then swipe RFID card')

    args = parser.parse_args()

    jukebox = JukeBox(args.i, args.db)

    if args.a is not None:
        jukebox.add_new_mp3(args.a)
    else:
        jukebox.start()