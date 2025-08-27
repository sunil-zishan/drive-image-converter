from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Step 1: Authenticate using your downloaded JSON
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',  # Replace with your actual filename if different
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)
creds = flow.run_local_server(port=0)

# Step 2: Build the Drive service
service = build('drive', 'v3', credentials=creds)

# Step 3: Define your shared folder ID

# Original folder for production use:
# folder_id = '1UnIvVB71Wx0QIytCMBYAg0EeDgM9cLU1'

# Sample test folder for development:
folder_id = '1-7yLP3QMAI_QFCkceKC6uH5x5C_GPBpD'


# Step 4: List files in the folder
def list_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

# Step 5: Print the results
files = list_files(service, folder_id)
for file in files:
    print(f"{file['name']} ({file['id']}) - {file['mimeType']}")
