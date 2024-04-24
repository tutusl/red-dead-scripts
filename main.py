import os
import time
import json
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constants
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = '1oKIJpxeINvirio80yZtd-xiaRraax27-dfp8pUzxRSQ'
RANGE = 'Página1!A1:Z100'
HTML_FILE_PATH = 'table.html'


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# Function to download the spreadsheet
def download_spreadsheet(service):
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE)
    response = request.execute()
    return response


# Function to convert spreadsheet data to HTML
def generate_html(data):
    df = pd.DataFrame(data['values'][1:], columns=data['values'][0])
    html = df.to_html(index=False)
    return html


# Function to save HTML file locally
def save_html(html_content):
    with open(HTML_FILE_PATH, 'w') as html_file:
        html_file.write(html_content)
    print(f"HTML file saved to {HTML_FILE_PATH}")


# Main function
def main():
    # Authenticate with Google Drive API
    creds = authenticate()
    service = build("sheets", "v4", credentials=creds)

    # Initial download of the spreadsheet
    spreadsheet_data = download_spreadsheet(service)
    html_content = generate_html(spreadsheet_data)
    save_html(html_content)


if __name__ == '__main__':
    main()
