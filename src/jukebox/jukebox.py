#!/usr/bin/env python3


import argparse
import logging
import subprocess

def play_file(sound_file_path):
    """
    @param sound_file_path:
    """
    pass


def read_rfid_input():
    """
    Read RFID reader input
    """

    rfid_code = input()
    print(rfid_code)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='JukeBox.')
    parser.add_argument('--db',
                        type=str,
                        help='Path to RFID - MP3 library',
                        required=True)

    parser.add_argument('-t', action='store_true',
                        help='Test mode')

    args = parser.parse_args()

    read_rfid_input()