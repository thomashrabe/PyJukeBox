#!/usr/bin/env python3


import argparse
import logging
import subprocess

from evdev import InputDevice, categorize, ecodes

def play_file(sound_file_path):
    """
    :param sound_file_path:
    """
    pass

def convert_event_strings_to_code(event_strings: [str]) -> str:
    """
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

def trigger_action_for_event_strings(event_strings: [str]):
    """
    Do something
    :param event_strings:
    """

    code = convert_event_strings_to_code(event_strings)
    print(code)


def rfid_input_loop(rfid_device_path: str):
    """
    Read RFID reader input in a loop, trigger actions when 
    a card was read.
    :param rfid_device_path:
    """

    device = InputDevice(rfid_device_path)

    chip_swiped = False
    trigger_action = False
    event_strings = []

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
                    trigger_action_for_event_strings(event_strings)
                except Exception as e:
                    logging.error('Failed trigger action')
                    logging.error(e)
                finally:
                    chip_swiped = False
                    trigger_action = False
                    event_strings = []

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

    rfid_input_loop(args.i)