from typing import Annotated
from datetime import date, datetime
from enum import Enum
from fastapi import APIRouter, Request, Path
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from .manage_itineraries import File
from ..handlers.google_drive import get_file
from ..handlers.google_sheets import (
    get_spreadsheet_data,
    append_sheet,
    update_row,
    delete_row,
)


class Category(str, Enum):
    activities = "activities"
    transportation = "transportation"
    housing = "housing"


class Resource(BaseModel):
    name: str
    index: int | None = None
    itinerary: str | None = None
    location_1: str | None = None
    location_2: str | None = None
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
                    "location_1": "Red Rock Canyon State Park",
                    "location_2": "Nightmare Gulch",
                    "cost": "6",
                    "date_start": "2024-11-30",
                    "date_end": "2024-11-30",
                }
            ]
        }
    }


class Data(BaseModel):
    activities: list[Resource] = []
    housing: list[Resource] = []
    transportation: list[Resource] = []


class Itinerary(File):
    data: Data


router = APIRouter()


@router.get("/{id}", response_model_exclude_none=True)
async def get_itinerary_activities(request: Request, id: str) -> Itinerary:
    file = get_file(request.app.credentials, id)

    activities = get_spreadsheet_data(
        request.app.credentials, spreadsheet_id=id, range_name="activities"
    )

    housing = get_spreadsheet_data(
        request.app.credentials, spreadsheet_id=id, range_name="housing"
    )

    transportation = get_spreadsheet_data(
        request.app.credentials, spreadsheet_id=id, range_name="transportation"
    )

    return {
        **file,
        "data": {
            "activities": activities,
            "housing": housing,
            "transportation": transportation,
        },
    }


@router.post("/{id}/{category}")
async def create_activity(
    request: Request, id: str, category: Category, body: Resource
):
    response = append_sheet(
        request.app.credentials,
        spreadsheet_id=id,
        sheet_name=category.value,
        data=jsonable_encoder([body]),
    )

    return response


@router.put("/{id}/{category}/{index}")
async def overwrite_activity(
    request: Request,
    id: str,
    index: int,
    category: Category,
    body: Resource,
):
    response = update_row(
        request.app.credentials,
        spreadsheet_id=id,
        sheet_name=category.value,
        index=index,
        data=jsonable_encoder(body),
    )

    return response


@router.delete("/{id}/{category}/{index}")
async def delete_activity(
    request: Request,
    id: str,
    index: int,
    category: Category,
):
    response = delete_row(
        request.app.credentials,
        spreadsheet_id=id,
        sheet_name=category.value,
        index=index,
    )

    return response
