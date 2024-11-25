from fastapi import FastAPI

from .api import api


app = FastAPI()

app.mount("/api", api)
