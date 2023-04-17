import serial
import time
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'creds.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Set up serial connection to Arduino sensor
ser = serial.Serial('/dev/ttyACM0', 9600)

# Set up Google Sheets API client
sheet_id = '1S23XuWeO-dSFv-0Er-zCOqd5yfPLg082cW622eZtG1Y'
sheet_range = 'Sheet1!A:B'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Loop to read data from sensor and write it to the sheet
while True:
    try:
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

        # Print debug information
        print(f"Data: {data}")
        print(f"Values: {values}")
        print("Data written to sheet.")

    except Exception as e:
        print(f"Error: {e}")

    # Wait for some time before reading again
    time.sleep(5)
