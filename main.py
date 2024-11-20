import os
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()
itineraries_folder_id = os.getenv("ITINERARIES_FOLDER_ID")
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")
template_spreadsheet_id = os.getenv("TEMPLATE_SPREADSHEET_ID")

app = FastAPI()


@app.get("/itineraries")
def get_itineraries():
    return {"message": "List of itineraries"}


@app.post("/itineraries")
def create_itinerary():
    return {"message": "Create an itinerary"}


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
