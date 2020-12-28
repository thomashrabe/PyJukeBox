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
async def read_db(folder_name: str):
    return jb_music_path_for_folder(folder_name)

