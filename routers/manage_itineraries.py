from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr

from ..handlers.google_drive import list_spreadsheets, copy_file, share_file, move_file


class Metadata(BaseModel):
    name: str
    email: EmailStr


router = APIRouter()


@router.get("")
async def get_itineraries(request: Request):
    response = list_spreadsheets(
        request.app.credentials, parent=request.app.folders["Itineraries"]
    )
    return response


@router.post("")
async def create_itinerary(request: Request, body: Metadata):
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
