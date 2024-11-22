from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def bootstrap_spreadsheet(credentials, spreadsheet_id):
    try:
        service = build("sheets", "v4", credentials=credentials)

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
        header_rows = [
            {
                "values": [
                    "name",
                    "itinerary",
                    "location",
                    "location_detail",
                    "date_start",
                    "date_end",
                    "cost",
                    "notes",
                ],
                "range_name": "activities",
            },
            {
                "values": [
                    "name",
                    "itinerary",
                    "location",
                    "location_detail",
                    "date_start",
                    "date_end",
                    "cost",
                    "notes",
                ],
                "range_name": "housing",
            },
            {
                "values": [
                    "name",
                    "itinerary",
                    "location_from",
                    "location_to",
                    "date_start",
                    "date_end",
                    "cost",
                    "notes",
                ],
                "range_name": "transportation",
            },
        ]

        for header in header_rows:
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=header["range_name"],
                valueInputOption="USER_ENTERED",
                body={"values": [header["values"]]},
            ).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_spreadsheet_data(credentials, spreadsheet_id, range_name):
    try:
        service = build("sheets", "v4", credentials=credentials)

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

        return [dict(zip(header, row)) for row in data]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
