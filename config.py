import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

# Get service account info from Streamlit secrets
service_account_info = dict(st.secrets["gcp_service_account"])

# Fix newlines in private key if needed
if '\\n' in service_account_info['private_key']:
    service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')

# Authenticate
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_NAME = "KONVERSI JATENG"
sheet = client.open(SHEET_NAME).sheet1
