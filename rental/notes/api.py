from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from rental.notes.exceptions import validate_note_and_handle_errors
from rental.notes.features import create_note
from rental.notes.features import delete_note
from rental.notes.features import get_note
from rental.notes.features import get_notes
from rental.notes.features import update_note
from rental.notes.models import Note
from rental.notes.serializer import CreateNoteSerializer
from rental.notes.serializer import NoteSerializer
from rental.notes.serializer import UpdateNoteSerializer
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateNotesView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            search_contract = request.query_params.get("contract")
            notes_list = get_notes(search_contract)

            paginator = self.pagination_class()
            paginated_notes = paginator.paginate_queryset(notes_list, request)
            serialized_list = NoteSerializer(paginated_notes, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request: Request):
        serializer = CreateNoteSerializer(data=request.data)
        # validate_note_and_handle_errors(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteANoteView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, note_id):
        note = get_note(note_id)

        serialized_note = NoteSerializer(note)

        return Response(serialized_note.data, status=status.HTTP_200_OK)

    def put(self, request: Request, note_id: int):
        note = Note.objects.filter(id=note_id).first()
        serializer = UpdateNoteSerializer(
            note,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, note_id):
        delete_note(note_id)
        return Response(status=status.HTTP_200_OK)
