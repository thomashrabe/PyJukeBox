#!/usr/bin/env python3

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from config import (
    jb_real_path_for_folder,
    jb_music_path_for_folder)
from jukebox.db import (
    read_jbdb, create_new_folder)

jukeboxBackend = FastAPI()

origins = [
    "http://localhost:8080"
]

jukeboxBackend.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def result_generator(result: str, msg: str) -> dict:
    """
    Generate a result message
    @param result: Either 'success' or 'error'
    @param msg: Message to send with details
    """

    if not result in ['success', 'error']:
        return {
            'result': 'error',
            'msg': 'Failure in result_generator'
        }

    return {'result': result, 'msg': msg}


def success_generator(msg: str) -> dict:
    """
    Generate an success message
    @param msg: Message to send with details
    """
    return result_generator('success', msg)


def error_generator(error: str) -> dict:
    """
    Generate an error message
    @param error: Error string
    """
    return result_generator('error', error)

@jukeboxBackend.get("/")
async def root():
    return {"message": "PyJukebox"}

@jukeboxBackend.get("/db")
async def read_db():
    return read_jbdb('/jukebox/db.jbdb')

@jukeboxBackend.get("/addFolder/{new_folder_name}")
async def add_folder(folder_name: str):
    create_new_folder(folder_name)

    try:
        create_new_folder(
            new_folder_name,
            '/jukebox/db.jbdb')
        return success_generator('Folder created')
    except Exception as e:
        return error_generator(str(e))

@jukeboxBackend.post("/addFiles/{folder_name}/{file_name}")
async def add_folder(folder_name: str):
    print('Add file')
    print(file_name)
    return jb_music_path_for_folder(folder_name)

@jukeboxBackend.get("/rmFolder/{folder_name}")
async def rm_folder(folder_name: str):
    print('Rm folder')
    print(folder_name)
    return jb_music_path_for_folder(folder_name)

@jukeboxBackend.get("/rmFile/{folder_name}/{file_name}")
async def rm_file(folder_name: str, file_name: str):
    print('Rm file')
    print(file_name)
    return jb_music_path_for_folder(folder_name)

@jukeboxBackend.get("/assignRFID/{folder_name}")
async def assignRFID(folder_name: str):
    """
    Trigger RFID wait on swipe
    @param folder_name: Name that will be assigned to RFID chip
    """
    return "PASS"


