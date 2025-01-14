from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException


def bootstrap_spreadsheet(credentials, spreadsheet_id):
    with build("sheets", "v4", credentials=credentials) as service:
        try:
            # create sheets
            requests = [
                {"addSheet": {"properties": {"title": "activities", "index": 0}}},
                {"addSheet": {"properties": {"title": "housing", "index": 1}}},
                {"addSheet": {"properties": {"title": "transportation", "index": 2}}},
                {"deleteSheet": {"sheetId": 0}},
            ]
            body = {"requests": requests}

            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id, body=body
            ).execute()

            # add headers to each sheet
            columns = [
                "name",
                "itinerary",
                "location_1",
                "location_2",
                "date_start",
                "date_end",
                "cost",
                "notes",
            ]
            sheet_names = ["activities", "transportation", "housing"]

            for sheet in sheet_names:
                service.spreadsheets().values().append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet,
                    valueInputOption="RAW",
                    body={"values": [columns]},
                ).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


def get_spreadsheet_data(credentials, spreadsheet_id, range_name):
    with build("sheets", "v4", credentials=credentials) as service:
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            rows = result.get("values", [])
            print(f"{len(rows)} rows retrieved")

            header = rows[0]
            data = rows[1:]

            return [
                {
                    "index": index + 1,
                    **dict([key, value] for (key, value) in zip(header, row) if value),
                }
                for (index, row) in enumerate(data)
            ]

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise HTTPException(status_code=error.resp.status)


def append_sheet(credentials, spreadsheet_id, sheet_name, data):
    with build("sheets", "v4", credentials=credentials) as service:
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!1:1")
                .execute()
            )

            header = result.get("values", [])[0]
            body = {
                "values": [[row.get(field, None) for field in header] for row in data]
            }

            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )

            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise HTTPException(status_code=error.resp.status)


def update_row(credentials, spreadsheet_id, sheet_name, index, data):
    with build("sheets", "v4", credentials=credentials) as service:
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!1:1")
                .execute()
            )

            header = result.get("values", [])[0]
            body = {"values": [[data.get(field, None) for field in header]]}

            range = f"{sheet_name}!{index + 1}:{index + 1}"

            result = (
                service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )

            print(f"{(result.get('updatedRows'))} rows updated.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise HTTPException(status_code=error.resp.status)


def delete_row(credentials, spreadsheet_id, sheet_name, index):
    with build("sheets", "v4", credentials=credentials) as service:
        try:
            # Retrieve sheet id
            request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
            response = request.execute()

            sheets = response["sheets"]
            sheet_id = [
                sheet["properties"]["sheetId"]
                for sheet in sheets
                if sheet["properties"]["title"] == sheet_name
            ][0]

            # Delete dimension
            request_body = {
                "requests": [
                    {
                        "deleteDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                "startIndex": index,
                                "endIndex": index + 1,
                            }
                        }
                    }
                ]
            }

            result = (
                service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
                .execute()
            )

            print(f"Deleted rows.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise HTTPException(status_code=error.resp.status)


def clear_sheet(credentials, spreadsheet_id, sheet_name):
    range_name = f"{sheet_name}!A2:Z"

    with build("sheets", "v4", credentials=credentials) as service:
        try:
            response = (
                service.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            return response
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
