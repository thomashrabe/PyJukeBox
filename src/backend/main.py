#!/usr/bin/env python3

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from config import (
    jb_real_path_for_folder,
    jb_music_path_for_folder)
from jukebox.db import read_jbdb

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

@jukeboxBackend.get("/")
async def root():
    return {"message": "PyJukebox"}

@jukeboxBackend.get("/db")
async def read_db():
    return read_jbdb('/jukebox/db.jbdb')

@jukeboxBackend.get("/addFolder/{folder_name}")
async def add_folder(folder_name: str):
    print('Add folder')
    print(folder_name)
    return jb_music_path_for_folder(folder_name)

@jukeboxBackend.post("/addFile/{folder_name}/{file_name}")
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


