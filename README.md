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

Save service account credentials to `credentials.json`.

Run the FastAPI dev server:

```shell
fastapi dev main.py
```
