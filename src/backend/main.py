#!/usr/bin/env python3

from fastapi import FastAPI

from jukebox.db import read_jbdb

jukeboxBackend = FastAPI()

@jukeboxBackend.get("/")
async def root():
    return {"message": "PyJukebox"}

@jukeboxBackend.get("/db")
async def read_db():
    return read_jbdb('/jukebox/db.jbdb')

