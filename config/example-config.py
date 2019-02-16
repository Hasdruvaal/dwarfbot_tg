# Telegram
tg_proxy = {
    # 'https': 'socks5://user:password@ip:port',
    'https': 'socks5h://user:password@ip:port',
    'http': 'http://user:password@ip:port'
}
# Keep it empty if you not need it
tg_token = 'get_it_from_@BotFather'
# Your bot token

# DB
db_name = 'db'
db_user = 'username'
db_pass = 'password'
db_host = '127.0.0.1'
db_port = 5432

# Google
scopes = [  # Scopes from goggle-example
            'https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive.readonly',
            # Scopes from docs-create-sample
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            # Scopes from ...
            'https://www.googleapis.com/auth/drive.appdata']
# Scopes defines previligies of google-app, no needs to edit it

secret_file = 'config/google_secret.json'
# you can get it in google-api developer console:
# https://console.developers.google.com/apis/credentials/consent
root_folder = '1JXLfpZXX7jphntXiBgzevgi3b2mZ9ODp'
# copy it from url of your google drive folder
# go to drive.google.com open destination folder
# for me its https://drive.google.com/drive/folders/1JXLfpZXX7jphntXiBgzevgi3b2mZ9ODp

# ImGur
imgur_key = 'your_imgur_apikey'
imgur_secret = 'your_imgur_secret'
