from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

# Load credentials
KEY_FILE = 'europafoodxb-450709-83ad97f31d8c.json'  # Replace this with your JSON key file name
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SITE_URL = 'https://europafoodxb.com/'  # Replace this with your actual GSC verified domain

# Authenticate
credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=credentials)

# API request
request = {
    'startDate': '2024-01-01',
    'endDate': '2024-03-31',
    'dimensions': ['page'],
    'rowLimit': 25000
}

response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()

rows = response.get('rows', [])
data = [{
    'page': row['keys'][0],
    'clicks': row.get('clicks', 0),
    'impressions': row.get('impressions', 0),
    'ctr': row.get('ctr', 0),
    'position': row.get('position', 0)
} for row in rows]

df = pd.DataFrame(data)
df.to_csv('gsc_export.csv', index=False)
print(f"Exported {len(df)} rows to gsc_export.csv")
