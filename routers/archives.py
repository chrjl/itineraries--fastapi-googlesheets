from fastapi import APIRouter, HTTPException, Request
from ..handlers.google_drive import list_spreadsheets, get_parent_ids, delete_file

router = APIRouter()


@router.get("")
def get_archived_itineraries(request: Request):
    response = list_spreadsheets(
        request.app.credentials, parent=request.app.folders["Archives"]
    )
    return response


@router.delete("/{id}")
def permanently_delete_archived_itinerary(request: Request, id: str):
    response = get_parent_ids(request.app.credentials, file_id=id)
    parent = response.get("parents", [])[0]

    if parent != request.app.folders["Archives"]:
        raise HTTPException(
            status_code=403, detail="Attempting to delete an active itinerary"
        )

    response = delete_file(request.app.credentials, id)

    return response
