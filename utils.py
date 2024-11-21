import os
import json

from dotenv import load_dotenv

load_dotenv()

from handlers.google_auth import get_credentials
from handlers.google_drive import list_files, delete_file

credentials = get_credentials(os.getenv("SERVICE_ACCOUNT_FILE"))

response = list_files(credentials)
print(json.dumps(response, indent=2))

while file_id := input("Delete file: "):
    delete_file(credentials, file_id)
