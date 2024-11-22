import os
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from dotenv import load_dotenv

load_dotenv()
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")


from handlers.google_auth import get_credentials
from handlers.google_drive import (
    list_folders,
    list_spreadsheets,
    copy_file,
    share_file,
    list_spreadsheets,
)

app = FastAPI()
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


class Metadata(BaseModel):
    name: str
    email: EmailStr


@app.get("/itineraries")
async def get_itineraries():
    response = list_spreadsheets(credentials, parent=folders["Itineraries"])
    return response


@app.post("/itineraries")
async def create_itinerary(body: Metadata):
    response = copy_file(
        credentials,
        file_id=template_id,
        name=body.name,
        parent_id=folders["Itineraries"],
    )

    share_file(credentials, file_id=response["id"], email_address=body.email)

    return response


@app.delete("/itineraries/{itinerary_id}")
def archive_itinerary():
    return {"message": "Archive an itinerary"}


@app.get("/itineraries/{itinerary_id}")
def get_itinerary():
    return {"message": "Get an itinerary"}


@app.patch("/itineraries/{itinerary_id}")
def update_itinerary():
    return {"message": "Update an itinerary"}


@app.get("/archives", tags=["archives"])
def get_archived_itineraries():
    return {"message": "Get an itinerary"}


@app.get("/archives/{itinerary_id}", tags=["archives"])
def get_archived_itinerary():
    return {"message": "Get an itinerary"}
