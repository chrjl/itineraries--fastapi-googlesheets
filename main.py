from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api import api


app = FastAPI()

app.mount("/api", api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
