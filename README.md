📦 drive-image-converter
A Python-based utility that syncs image files from Google Drive, converts them to HEIC format using ImageMagick, and re-uploads them — replacing the originals. Designed for efficient image storage and format standardization.

🚀 Features
🔐 OAuth2 authentication with Google Drive

📂 Recursively scans folders and subfolders for .jpg, .jpeg, and .png files

🖼️ Converts images to .heic using ImageMagick

☁️ Uploads converted images back to the same Drive folder

🧹 Deletes original files and cleans up local temp files

🛠️ Tech Stack
Python 3.10+

Google Drive API

ImageMagick with HEIC support (libheif)

Docker (optional)

📁 Project Structure
Code
heic_converter/
├── convert.py              # Conversion logic (optional)
├── drive_sync.py           # Main sync and conversion script
├── drive_list_files.py     # Utility for listing files
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup (if needed)
├── client_secret.json      # OAuth credentials (excluded via .gitignore)
├── token.json              # Auth token (excluded via .gitignore)
└── .gitignore              # Keeps sensitive and temp files out of Git
⚙️ Setup Instructions
Clone the repo

bash
git clone https://github.com/sunil-zishan/drive-image-converter.git
cd drive-image-converter
Create a virtual environment

bash
python3 -m venv drive-sync-env
source drive-sync-env/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Install ImageMagick with HEIC support

macOS: brew install imagemagick libheif

Ubuntu: sudo apt install imagemagick libheif-dev

Add your Google API credentials

Place client_secret.json in the root directory.

▶️ Usage
Run the sync and conversion script:

bash
python drive_sync.py
You’ll be prompted to authenticate via Google OAuth. Once authorized, the script will:

Download eligible images to /tmp/

Convert them to .heic

Upload them to the same Drive folder

Delete the originals

Clean up local temp files

🧼 .gitignore Highlights
Sensitive and temp files are excluded:

Code
token.json
client_secret.json
/tmp/
drive-sync-env/
__pycache__/
📜 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute.
