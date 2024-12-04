import os
import pickle #a file that stores authentication - once authenticated once user wont have to again
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText



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
        if creds and creds.expired and creds.refresh_token: #check if creds exists but is expired
            creds.refresh(Request())
        else:
            # Set up the OAuth 2.0 flow (opens a browser window for user authentication)
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Launches the authentication flow

        #save creds
        with open("pickle.token","wb") as token:
            pickle.dump(creds,token)
    serviceGmail = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    serviceContacts = googleapiclient.discovery.build('people','v1',credentials=creds)
    serviceCalander = googleapiclient.discovery.build('calendar','v3',credentials=creds)
    return [serviceGmail,serviceContacts,serviceCalander]

def send_email_gmail(service, to_email, subject, text):
    #Create mime email address
    message = MIMEText(text)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    #send the email
    try:
        send_message = (service.users().messages().send(userId="me", body={"raw": raw_message}).execute())
        print(f"successfuly sent message! ID:{send_message["id"]}")
    except Exception as E:
        print(E)

def list_google_contacts(service):
    try:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,  # Number of contacts to fetch - 1000 is max
            personFields='names,emailAddresses'  # Specify fields you want
        ).execute()
        connections = results.get('connections',[])
        contacts = dict()
        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses',[])

            contacts[names[0].get("displayName")] = emails[0].get("value")
        return contacts
    except Exception as e:
        print(e)
    
def add_contact(service, name, email):
    contact = {
        "names":[{"givenName":name}],
        "emailAddresses":[{"value":email}]
    }   
    service.people().createContact(body  = contact).execute()

def create_event(service,data):
    print(data)
    event = service.events().insert(calendarId="primary", body=data).execute()
    
    print(event.get('htmlLink'))

def get_events(service,data):
    print(data)

