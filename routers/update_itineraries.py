from typing import Literal
from datetime import date, datetime
from enum import Enum
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from .manage_itineraries import File
from ..handlers.google_drive import get_file
from ..handlers.google_sheets import get_spreadsheet_data, append_sheet, clear_sheet


class Category(str, Enum):
    activity = "activity"
    transportation = "transportation"
    housing = "housing"


class Resource(BaseModel):
    category: Category | str = Category.activity
    name: str
    itinerary: str | None = None
    location: str | None = None
    location_detail: str | None = None
    location_from: str | None = None
    location_to: str | None = None
    date_start: date | datetime | None = None
    date_end: date | datetime | None = None
    cost: float | None = None
    notes: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category": "activity",
                    "name": "Hiking",
                    "location": "Red Rock Canyon State Park",
                    "location_detail": "Nightmare Gulch",
                    "cost": "6",
                    "date_start": "2024-11-30",
                    "date_end": "2024-11-30",
                }
            ]
        }
    }


class Itinerary(File):
    data: list[Resource]


router = APIRouter()


@router.get("/{id}", response_model_exclude_none=True)
async def get_itinerary(request: Request, id: str) -> Itinerary:
    file = get_file(request.app.credentials, id)

    activities = [
        {"category": "activity", **activity}
        for activity in get_spreadsheet_data(
            request.app.credentials,
            spreadsheet_id=id,
            range_name="activities",
        )
    ]
    housing = [
        {"category": "housing", **housing}
        for housing in get_spreadsheet_data(
            request.app.credentials, spreadsheet_id=id, range_name="housing"
        )
    ]
    transportation = [
        {"category": "transportation", **transportation}
        for transportation in get_spreadsheet_data(
            request.app.credentials,
            spreadsheet_id=id,
            range_name="transportation",
        )
    ]

    return {**file, "data": [*activities, *housing, *transportation]}


@router.post("/{id}")
async def add_to_itinerary(request: Request, id: str, body: Resource):
    sheet_name = (
        "housing"
        if body.category == "housing"
        else "transportation" if body.category == "transportation" else "activities"
    )
    response = append_sheet(
        request.app.credentials,
        spreadsheet_id=id,
        sheet_name=sheet_name,
        data=jsonable_encoder([body]),
    )

    return response


@router.put("/{id}/{category}")
async def update_an_itinerary(
    request: Request, id: str, category: Category, body: list[Resource]
):
    sheet_name = (
        "housing"
        if category == Category.housing
        else "transportation" if category == Category.transportation else "activities"
    )

    clear_sheet(request.app.credentials, spreadsheet_id=id, sheet_name=sheet_name)

    response = append_sheet(
        request.app.credentials,
        spreadsheet_id=id,
        sheet_name=sheet_name,
        data=jsonable_encoder(body),
    )

    return response
