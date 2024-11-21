import os
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()
itineraries_folder_id = os.getenv("ITINERARIES_FOLDER_ID")
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")
template_spreadsheet_id = os.getenv("TEMPLATE_SPREADSHEET_ID")


from handlers.google_auth import get_credentials
from handlers.google_drive import (
    copy_file,
    share_file,
)

app = FastAPI()
credentials = get_credentials(service_account_file)


class Metadata(BaseModel):
    name: str
    email: EmailStr


@app.get("/itineraries")
def get_itineraries():
    return {"message": "List of itineraries"}


@app.post("/itineraries")
async def create_itinerary(body: Metadata):
    spreadsheet_id = copy_file(
        credentials,
        file_id=template_spreadsheet_id,
        name=body.name,
        parent_id=itineraries_folder_id,
    )

    share_file(credentials, file_id=spreadsheet_id, email_address=body.email)

    return {"spreadsheetId": spreadsheet_id}


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
