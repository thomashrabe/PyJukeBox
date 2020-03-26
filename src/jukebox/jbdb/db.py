import json

def read_jbdb(db_file_path: str):
    """
    Reads JukeBox db file
    :param db_file_path:
    """

    with open(db_file_path, 'r') as f:
        jbdb = json.load(f)

    return jbdb





