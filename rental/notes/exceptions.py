from rest_framework import status
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorNoteWithSameSubjectAlreadyExists(APIException):
    def __init__(self, subject: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Note with subject "{subject}" already exists'
        self.default_code = 'note-001'

class ErrorNoteInvalidSubject(APIException):
    def __init__(self, subject: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid subject "{subject}"'
        self.default_code = 'note-002'

class ErrorNoteInvalidBody(APIException):
    def __init__(self, body: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid body "{body}"'
        self.default_code = 'note-003'


def validate_note_and_handle_errors(serializer):
    serializer.is_valid()

    if 'subject' in serializer.errors:
        error_detail = serializer.errors['subject'][0]
        if error_detail.code == 'unique':
            raise ErrorNoteWithSameSubjectAlreadyExists(serializer.data.get('subject'))
        elif error_detail.code in ['invalid', 'required', 'blank']:
            raise ErrorNoteInvalidSubject(serializer.data.get('subject'))

    if 'body' in serializer.errors:
        error_detail = serializer.errors['body'][0]
        raise ErrorNoteInvalidBody(serializer.data.get('body'))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
