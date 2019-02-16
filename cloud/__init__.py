import config

from cloud.auth import CloudAuthData
from cloud.session import CloudSession
from cloud.service import DriveService, DocsService

authData = CloudAuthData(config.scopes, config.secret_file)
googleSession = CloudSession.google(authData)
googleDrive = DriveService(googleSession.creds)
googleDocs = DocsService(googleSession.creds)
