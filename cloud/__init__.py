import config

from cloud.auth import CloudAuthData
from cloud.session import CloudSession
from cloud.service import DriveService, DocsService

auth_data = CloudAuthData(config.scopes, config.secret_file)
google_session = CloudSession.google(auth_data)
google_drive = DriveService(google_session.creds)
google_docs = DocsService(google_session.creds)
