import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    creds = None
    token_path = "token.pickle"
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    try:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif not creds or not creds.valid:
            # The `client_secrets.json` file should be downloaded from the Google Cloud Console
            # and placed in the same directory as this script.
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES)
            
            # Indicate that a browser is not available
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"Please go to this URL and authorize access: {auth_url}")
            auth_code = input("Enter the authorization code: ")
            
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
    except RefreshError:
        print("Token expired or revoked. Deleting token.pickle and re-authenticating.")
        if os.path.exists(token_path):
            os.remove(token_path)
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json", SCOPES)
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        print(f"Please go to this URL and authorize access: {auth_url}")
        auth_code = input("Enter the authorization code: ")
        
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        # Save the credentials for the next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service

def create_label(service, label_name):
    """Crée un libellé dans Gmail."""
    label_body = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    try:
        label = service.users().labels().create(userId='me', body=label_body).execute()
        print(f"Libellé créé : {label['name']}")
        return label
    except Exception as e:
        print(f"Erreur lors de la création du libellé : {e}")
        return None

if __name__ == "__main__":
    service = get_gmail_service()
    print("Successfully connected to Gmail API.")
    # You can now use the 'service' object to interact with the Gmail API.
    # For example, to list labels:
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    # print('Labels:')
    # if not labels:
    #     print('No labels found.')
    # else:
    #     for label in labels:
    #         print(label['name'])
