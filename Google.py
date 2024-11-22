import os
import pickle #a file that stores authentication - once authenticated once user wont have to again
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

#These scopes are full access to gmail, contacts and calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',        # Full Gmail access (read and write)
    'https://www.googleapis.com/auth/contacts',            # Full access to Contacts (read and write)
    'https://www.googleapis.com/auth/calendar',            # Full access to Calendar (read and write)
]

def authenticate_google_api():
    creds = None
    if os.path.exists("pickle.token"):
        with open("pickle.token","rb") as token: #if the file exists load it as creds
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh.token: #check if creds exists but is expired
            creds.refresh(Request())
        else:
            # Set up the OAuth 2.0 flow (opens a browser window for user authentication)
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Launches the authentication flow

        #save creds
        with open("pickle.token","wb") as token:
            pickle.dump(creds,token)
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    return service

