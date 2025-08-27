import os
import io
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# 🔐 Scopes for full Drive access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate with Google Drive and return the service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def list_images(service, folder_id):
    """List image files in the specified Drive folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

def download_image(service, file_id, filename):
    """Download image from Drive to local path."""
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(filename, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

def convert_to_heic(input_path, output_path):
    """Convert image to HEIC using ImageMagick."""
    subprocess.run(['magick', input_path, output_path], check=True)

def upload_heic(service, folder_id, filename):
    """Upload HEIC file to Drive folder."""
    file_metadata = {
        'name': os.path.basename(filename),
        'parents': [folder_id]
    }
    media = MediaFileUpload(filename, mimetype='image/heic')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def delete_original(service, file_id):
    """Delete original image from Drive."""
    service.files().delete(fileId=file_id).execute()

def main():
# Original folder for production use:
# folder_id = '1UnIvVB71Wx0QIytCMBYAg0EeDgM9cLU1'

# Sample test folder for development:
    folder_id = '1-7yLP3QMAI_QFCkceKC6uH5x5C_GPBpD'
    service = authenticate()
    images = list_images(service, folder_id)

    for image in images:
        original_name = image['name']
        original_id = image['id']
        ext = os.path.splitext(original_name)[1].lower()

        if ext not in ['.jpg', '.jpeg', '.png']:
            print(f"Skipping unsupported file: {original_name}")
            continue

        safe_name = original_name.replace(' ', '_').replace('(', '').replace(')', '')
        input_path = f'/tmp/{safe_name}'
        output_name = os.path.splitext(safe_name)[0] + '.heic'
        output_path = f'/tmp/{output_name}'

        try:
            print(f"🔄 Processing: {original_name}")
            download_image(service, original_id, input_path)
            convert_to_heic(input_path, output_path)
            upload_heic(service, folder_id, output_path)
            delete_original(service, original_id)
            print(f"✅ Replaced {original_name} with {output_name}")
        except Exception as e:
            print(f"❌ Error processing {original_name}: {e}")

if __name__ == '__main__':
    main()
