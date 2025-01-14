import os
import json
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE") or "credentials.json"

from .routers import archives, manage_itineraries, update_itineraries
from .handlers.google_auth import get_credentials
from .handlers.google_drive import list_folders, list_spreadsheets

with open(service_account_file) as file:
    service_account_info = json.load(file)

# credentials = get_credentials(service_account_file=service_account_file)
credentials = get_credentials(service_account_info=service_account_info)

# find file ids
folders = dict([[folder["name"], folder["id"]] for folder in list_folders(credentials)])
template = [
    file
    for file in list_spreadsheets(credentials, folders["Templates"])
    if file["name"] == "Itinerary"
]

if "Itineraries" in folders:
    logger.debug(f"Found folder `Itineraries`: {folders["Itineraries"]}")
else:
    raise FileNotFoundError("Could not find `Itineraries` folder")

if "Archives" in folders:
    logger.debug(f"Found folder `Archives`   : {folders["Archives"]}")
else:
    raise FileNotFoundError("Could not find `Archives` folder")

if "Templates" in folders:
    logger.debug(f"Found folder `Templates`  : {folders["Templates"]}")
else:
    raise FileNotFoundError("Could not find `Templates` folder")

if template:
    template_id = template[0]["id"]
    logger.debug(f"Found spreadsheet `Templates/Itinerary`: {template_id}")
else:
    raise FileNotFoundError("Could not find template itinerary")


api = FastAPI()

api.credentials = credentials
api.folders = folders
api.template_id = template_id

api.include_router(manage_itineraries.router, prefix="/itineraries", tags=["itineraries"])
api.include_router(update_itineraries.router, prefix="/itineraries", tags=["activities"])
api.include_router(archives.router, prefix="/archives", tags=["archives"])
