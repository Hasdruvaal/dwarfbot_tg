scopes = [
            # Scopes from example
            'https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive.readonly',

            # Scopes from docs-create-sample
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',

            # Scopes from ...
            'https://www.googleapis.com/auth/drive.appdata',
        ]

secret_file = 'config/google_secret.json'
# you can get it in google-api developer console:
# https://console.developers.google.com/apis/credentials/consent

root_folder = '1JOLfpZ9C7jphntXiBrrevniyb2mZ8ODp'
# copy it from url of your google drive folder
# go to drive.google.com open destination folder
# for me its https://drive.google.com/drive/folders/1JOLfpZ9C7jphntXiBrrevniyb2mZ8ODp
