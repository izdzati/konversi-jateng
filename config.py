import gspread
from google.oauth2.service_account import Credentials

# Load Credentials dari JSON
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("konversi-jateng-984cb852b8dd.json", scopes=SCOPES)

# Autentikasi ke Google Sheets
client = gspread.authorize(creds)

# Akses Google Sheet
SHEET_NAME = "KONVERSI JATENG"
sheet = client.open(SHEET_NAME).sheet1
