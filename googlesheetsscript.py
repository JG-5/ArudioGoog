import serial
import time
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'cred.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Set up serial connection to Arduino sensor
ser = serial.Serial('/dev/ttyACM0', 9600)

# Set up Google Sheets API client
sheet_id = '1dNEaKV-teGvfsnebGzdR0PcJK4cyMgwO4KQCNNpExXk'
sheet_range = 'Sheet1!A:B'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Loop to read data from sensor and write it to the sheet
while True:
    # Read data from sensor
    data = ser.readline().decode().strip().split(',')

    # Format data for Google Sheets API
    values = [
        [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + data
    ]

    # Write data to sheet
    request_body = {
        'values': values
    }
    sheet.values().append(spreadsheetId=sheet_id, range=sheet_range,
                           valueInputOption='USER_ENTERED', body=request_body).execute()

    # Wait for some time before reading again
    time.sleep(5)
