# Trip Itinerary App

A FastAPI front-facing REST API that uses Google Sheets as a backend by interfacing with Google Workspace APIs (Google Drive, Google Sheets). Requires authorized service account credentials for the Google Cloud Project to be stored at `credentials.json`.

## Run the dev server

Create and enter venv:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

After [setting up the Google Cloud project](#setting-up-the-google-cloud-project):

- Save service account credentials to `credentials.json`.
- Store Google Drive file IDs for the following to environment (or `.env`):
  - `ITINERARIES_FOLDER_ID`
  - `ARCHIVES_FOLDER_ID`
  - `TEMPLATE_SPREADSHEET_ID`

Run the FastAPI dev server:

```shell
fastapi dev main.py
```

## Setting up the Google Cloud Project

- Create Google Cloud Project
- Enable APIs: Google Drive API, Google Sheets API
- Create service account
- Create service account key

### Bootstrapping the project

All files created will be owned by the service account and stored in its Google Drive. Active itineraries will be stored in the `Itineraries` folder and archived itineraries will be stored in the `Itineraries/Archives` folder. A template spreadsheet stored in `Itineraries/Templates` will be used to create new itineraries. All folders need to be created and shared with the project owner.

A migration script performs the following:

- Create `Itineraries` folder.
- Share `Itineraries` folder with project owner. Permissions will propagate.
- Create `Archives` folder in `Itineraries` folder.
- Create `Templates` folder in `Itineraries` folder.
- Create `Template Itinerary` spreadsheet in `Templates` folder.

Run the migration script:

```shell
python migration.py
```

And store the returned file IDs in their corresponding environment variables:

- `ITINERARIES_FOLDER_ID`
- `ARCHIVES_FOLDER_ID`
- `TEMPLATE_SPREADSHEET_ID`

## How it works

Creating a new itinerary copies the template itinerary spreadsheet into a new spreadsheet in the active itineraries folder and shares it with the requester. Archiving an itinerary moves the itinerary spreadsheet into the archives folder.
