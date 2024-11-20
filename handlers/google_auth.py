from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_credentials(service_account_file):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    return credentials
