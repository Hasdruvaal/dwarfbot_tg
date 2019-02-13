from googleapiclient.discovery import build

class BaseService:
    def __init__(self, creditionals):
        self.creditionals = creditionals
        self.service = build(self.service_name, self.api_version, credentials=self.creditionals)
