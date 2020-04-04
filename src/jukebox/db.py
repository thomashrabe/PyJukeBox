import os
import json
import glob

def read_jbdb(db_file_path: str) -> {}:
    """
    Reads JukeBox db file
    :param db_file_path:
    """

    if not os.path.exists(db_file_path):
        msg = '{} does not exist!'.format(db_file_path)
        raise IOError(msg)

    with open(db_file_path, 'r') as f:
        jbdb = json.load(f)

    return jbdb

def add_new_file(db_file_path: str, code: str, new_data_path:str) -> None:
    """
    :param db_file_path:
    :param cod:
    :param new_data_path:
    """

    if not os.path.exists(new_data_path):
        msg = '{} does not exist!'.format(new_data_path)
        raise IOError(msg)

    db = read_jbdb(db_file_path)

    if os.path.isfile(new_data_path):
        db[code] = new_data_path
    elif os.path.isdir(new_data_path):
        files1 = glob.glob(os.path.join(new_data_path, '*.mp3'))
        files2 = glob.glob(os.path.join(new_data_path, '*.m4a'))
        files3 = glob.glob(os.path.join(new_data_path, '*.MP3'))

        files = files1 + files2 + files3

        new_files = []
        for a_file in files:
            new_file_path = os.path.abspath(a_file)
            new_files.append(new_file_path)

        db[code] = new_files

    with open(db_file_path, 'w') as f:
        json.dump(db, f, sort_keys=True, indent=4, separators=(',', ': '))


def lookup_item_for_rfid_code(rfid_code: str, db_file_path: str) -> str:
    """
    Returns items stored in DB behind RFID code
    :param rfid_code:
    :param db_file_path:
    :return:
    """

    db = read_jbdb(db_file_path)
    return db.get(rfid_code)

def get_confirmation_sound_path(db_file_path: str):
    """
    Returns path to confirmation sound
    :param db_file_path:
    """
    db = read_jbdb(db_file_path)
    return db.get('confirmation')