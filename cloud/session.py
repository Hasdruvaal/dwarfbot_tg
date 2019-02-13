from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils.cache import cached
import config.google as config

from cloud.auth import CloudAuthData

class CloudSession:
    def __init__(self, authData, secret_file='google_credentials.json'):
        self.creds = None
        self.authData = authData
        self.prepare_session()

    def prepare_session(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.update_session()
            else:
                self.create_session()

    def update_session(self):
        self.creds.refresh(Request)

    def create_session(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.authData.secret_file, self.authData.scopes)
        self.creds = flow.run_local_server()

    @cached
    def get_google_data(authData: CloudAuthData):
        return CloudSession(authData)
