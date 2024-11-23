import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")

from .routers import archives, manage_itineraries, update_itineraries
from .handlers.google_auth import get_credentials
from .handlers.google_drive import list_folders, list_spreadsheets

credentials = get_credentials(service_account_file)

# find file ids
folders = dict([[folder["name"], folder["id"]] for folder in list_folders(credentials)])

print(f"Found folders: {','.join(folders.keys())}")

template_id = [
    file
    for file in list_spreadsheets(credentials, folders["Templates"])
    if file["name"] == "Itinerary"
][0]["id"]

print(f"Found spreadsheet: template itinerary")


app = FastAPI(root_path="/api")

app.credentials = credentials
app.folders = folders
app.template_id = template_id

app.include_router(manage_itineraries.router, prefix="/itineraries", tags=["manage"])
app.include_router(update_itineraries.router, prefix="/itineraries", tags=["update"])
app.include_router(archives.router, prefix="/archives", tags=["archives"])
