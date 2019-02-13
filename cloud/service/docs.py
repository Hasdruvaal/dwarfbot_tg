from datetime import datetime

from cloud.service import BaseService
from logging import error

class DocsService(BaseService):
    def __init__(self, *args, **kwargs):
        self.service_name = 'docs'
        self.api_version = 'v1'
        super().__init__(*args, **kwargs)

    def get_document(self, document_id):
        response = self.service.documents().get(documentId=document_id).execute()
        return response

    def batch_update(self, document_id, batch):
        body = {'requests': batch}
        return self.service.documents().batchUpdate(documentId=document_id, body=body).execute()

    def add_text(self, index, text):
        return {'insertText': {
                        'location': {
                            'index': index,
                        },
                        'text': text
                }}

    def add_image(self, index, image):
        return {'insertInlineImage': {
                    'location': { 'index': index },
                    'uri': image,
                    'objectSize': {'height': {'magnitude': 350,
                                              'unit': 'PT'},
                                    'width': {'magnitude': 350,
                                              'unit': 'PT'}
                                  }
                    }
                }

    def add_data(self, document_id, owner, text=None, image=None):
        if not text and not image:
            error('No data to add')
            return

        batch = []
        index = self.get_document(document_id).get('body').get('content')[-1].get('endIndex')-1 or 1

        text_out = '\n\n'
        batch.append(self.add_text(index, text_out))
        if text:
            batch.append(self.add_text(index, text))
        if image:
            batch.append(self.add_text(index, '\n'))
            batch.append(self.add_image(index, image))
        text_in = '\n\n'+datetime.now().strftime('%d-%m-%Y %H:%M')+' '+owner+':\n'
        batch.append(self.add_text(index, text_in))
        return self.batch_update(document_id, batch)
