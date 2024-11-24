from datetime import date, datetime
from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr

from ..handlers.google_drive import list_spreadsheets, copy_file, share_file, move_file


class File(BaseModel):
    name: str
    id: str
    kind: str | None = None
    mimeType: str | None = None
    createdTime: date | datetime | None = None
    modifiedTime: date | datetime | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Test Itinerary",
                    "id": "159YsZTIXvW5GbKNQnI9LSqPqmXhWoxIl_59YpisKrxM",
                    "kind": "drive#file",
                    "mimeType": "application/vnd.google-apps.spreadsheet",
                    "createdTime": "2024-11-22T15:29:44.226000Z",
                    "modifiedTime": "2024-11-24T15:39:20.537000Z",
                }
            ]
        }
    }


class Metadata(BaseModel):
    name: str
    email: EmailStr


router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_itineraries(request: Request) -> list[File]:
    response = list_spreadsheets(
        request.app.credentials, parent=request.app.folders["Itineraries"]
    )
    return response


@router.post("", response_model_exclude_none=True)
async def create_itinerary(request: Request, body: Metadata) -> File:
    response = copy_file(
        request.app.credentials,
        file_id=request.app.template_id,
        name=body.name,
        parent_id=request.app.folders["Itineraries"],
    )

    share_file(
        request.app.credentials, file_id=response["id"], email_address=body.email
    )

    return response


@router.delete("/{id}")
async def archive_itinerary(request: Request, id: str):
    response = move_file(
        request.app.credentials,
        file_id=id,
        parent_id=request.app.folders["Archives"],
    )
    return response
