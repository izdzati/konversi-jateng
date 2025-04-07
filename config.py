import gspread
import json
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Ambil secret dari Streamlit
service_account_info = json.loads(st.secrets["gcp_service_account"])

# Autentikasi
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_NAME = "KONVERSI JATENG"
sheet = client.open(SHEET_NAME).sheet1
