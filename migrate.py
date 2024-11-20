from dotenv import load_dotenv
import os
import json

from handlers.google_auth import get_credentials
from handlers.google_drive import (
    create_folder,
    create_spreadsheet,
    list_files,
    delete_file,
    share_file,
)
from handlers.google_sheets import bootstrap_spreadsheet


load_dotenv()

credentials = get_credentials(os.getenv("SERVICE_ACCOUNT_FILE"))


if __name__ == "__main__":
    # create google drive folders
    itineraries_folder_id = create_folder(credentials=credentials, name="Itineraries")
    share_file(
        credentials=credentials,
        file_id=itineraries_folder_id,
        email_address=os.getenv("PROJECT_OWNER"),
        role="writer",
    )

    archives_folder_id = create_folder(
        credentials=credentials, name="Archives", parent=itineraries_folder_id
    )
    templates_folder_id = create_folder(
        credentials=credentials, name="Templates", parent=itineraries_folder_id
    )

    # create template itinerary
    template_spreadsheet_id = create_spreadsheet(
        credentials, name="Template Itinerary", parent=templates_folder_id
    )
    bootstrap_spreadsheet(credentials, template_spreadsheet_id)

    response = list_files(credentials=credentials)
    print(json.dumps(response, indent=2))
