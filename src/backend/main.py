#!/usr/bin/env python3

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

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

