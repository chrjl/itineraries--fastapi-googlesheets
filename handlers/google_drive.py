from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_file(credentials, name, mime_type, parent=None):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {
            "name": name,
            "mimeType": mime_type,
            "parents": [parent],
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'File ID: "{file.get("id")}".')
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def create_folder(credentials, name, parent=None):
    return create_file(credentials, name, "application/vnd.google-apps.folder", parent)


def create_spreadsheet(credentials, name, parent=None):
    return create_file(
        credentials, name, "application/vnd.google-apps.spreadsheet", parent
    )


def copy_file(credentials, file_id, name, parent_id=None):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {
            "name": name,
            "parents": [parent_id],
        }

        # pylint: disable=maybe-no-member
        file = service.files().copy(body=file_metadata, fileId=file_id).execute()
        print(f'File ID: "{file.get("id")}".')
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def list_files(credentials):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=credentials)
        response = service.files().list().execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    return response["files"]


def list_spreadsheets(credentials, parent=None):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=credentials)
        response = (
            service.files()
            .list(
                q=(
                    "mimeType='application/vnd.google-apps.spreadsheet'"
                    + (f" and '{parent}' in parents" if parent else "")
                )
            )
            .execute()
        )

    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    return response["files"]


def delete_file(credentials, file_id):
    service = build("drive", "v3", credentials=credentials)
    response = service.files().delete(fileId=file_id).execute()

    return response


def share_file(credentials, file_id, email_address, role="reader"):
    user_permission = {"type": "user", "role": role, "emailAddress": email_address}
    service = build("drive", "v3", credentials=credentials)
    response = (
        service.permissions().create(fileId=file_id, body=user_permission).execute()
    )

    return response