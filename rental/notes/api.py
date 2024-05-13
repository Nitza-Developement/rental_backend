from rest_framework import status
from rest_framework.response import Response
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from settings.utils.exceptions import BadRequest400APIException
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.notes.exceptions import validate_note_and_handle_errors
from rental.notes.features import create_note, get_notes, get_note, update_note, delete_note
from rental.notes.serializer import CreateNoteSerializer, NoteSerializer, UpdateNoteSerializer


class ListAndCreateNotesView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            notes_list = get_notes()

            paginator = self.pagination_class()
            paginated_notes = paginator.paginate_queryset(notes_list, request)
            serialized_list = NoteSerializer(paginated_notes, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateNoteSerializer(data=request.data)
        validate_note_and_handle_errors(serializer)

        created_note = create_note(
            contract_id=serializer.validated_data['contract'],
            user_id=serializer.validated_data['user'],
            subject=serializer.validated_data['subject'],
            body=serializer.validated_data['body'],
            remainder=serializer.validated_data.get('remainder'),
            file=serializer.validated_data.get('file'),
        )

        serialized_note = NoteSerializer(created_note)

        return Response(serialized_note.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteANoteView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, note_id):
        note = get_note(note_id)

        serialized_note = NoteSerializer(note)

        return Response(serialized_note.data, status=status.HTTP_200_OK)

    def put(self, request, note_id):
        serializer = UpdateNoteSerializer(data={
            'id': note_id,
            'subject': request.data.get('subject'),
            'body': request.data.get('body'),
            'remainder': request.data.get('remainder'),
            'file': request.data.get('file'),
        })
        validate_note_and_handle_errors(serializer)

        updated_note = update_note(
            note_id=note_id,
            subject=serializer.validated_data.get('subject'),
            body=serializer.validated_data.get('body'),
            remainder=serializer.validated_data.get('remainder'),
            file=serializer.validated_data.get('file'),
        )
        serialized_note = NoteSerializer(updated_note)

        return Response(serialized_note.data, status=status.HTTP_200_OK)

    def delete(self, request, note_id):
        delete_note(note_id)
        return Response(status=status.HTTP_200_OK)
