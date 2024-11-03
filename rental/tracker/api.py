from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.tracker.exceptions import validate_tracker_and_handle_errors
from rental.tracker.exceptions import validate_tracker_heartbeat_data_and_handle_errors
from rental.tracker.features import create_tracker
from rental.tracker.features import create_tracker_heart_beat_data
from rental.tracker.features import delete_tracker
from rental.tracker.features import delete_tracker_heart_beat_data
from rental.tracker.features import get_tracker
from rental.tracker.features import get_tracker_heart_beat_data
from rental.tracker.features import get_trackers
from rental.tracker.features import update_tracker
from rental.tracker.models import Tracker
from rental.tracker.serializer import CreateTrackerHeartBeatDataSerializer
from rental.tracker.serializer import CreateTrackerSerializer
from rental.tracker.serializer import TrackerHeartBeatDataSerializer
from rental.tracker.serializer import TrackerSerializer
from rental.tracker.serializer import UpdateTrackerSerializer
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateTrackersView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            trackers_list = get_trackers()

            paginator = self.pagination_class()
            paginated_trackers = paginator.paginate_queryset(trackers_list, request)
            serialized_list = TrackerSerializer(paginated_trackers, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateTrackerSerializer(data=request.data)
        validate_tracker_and_handle_errors(serializer)

        created_tracker = create_tracker(
            name=serializer.validated_data["name"],
            vehicle=serializer.validated_data["vehicle"],
        )

        serialized_tracker = TrackerSerializer(created_tracker)

        return Response(serialized_tracker.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteATrackerView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, tracker_id):
        tracker = get_tracker(tracker_id)

        serialized_tracker = TrackerSerializer(tracker)

        return Response(serialized_tracker.data, status=status.HTTP_200_OK)

    def put(self, request, tracker_id):
        tracker = Tracker.objects.filter(id=tracker_id).first()
        serializer = UpdateTrackerSerializer(
            tracker,
            data={
                "name": request.data.get("name"),
                "vehicle": request.data.get("vehicle"),
            },
        )
        validate_tracker_and_handle_errors(serializer)

        updated_tracker = update_tracker(
            tracker_id=tracker_id,
            name=serializer.validated_data.get("name"),
            vehicle=serializer.validated_data.get("vehicle"),
        )
        serialized_tracker = TrackerSerializer(updated_tracker)

        return Response(serialized_tracker.data, status=status.HTTP_200_OK)

    def delete(self, request, tracker_id):
        delete_tracker(tracker_id)
        return Response(status=status.HTTP_200_OK)


class ListAndCreateTrackerHeartBeatDataView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            heart_beat_data_list = get_tracker_heart_beat_data()

            paginator = self.pagination_class()
            paginated_heart_beat_data = paginator.paginate_queryset(
                heart_beat_data_list, request
            )
            serialized_list = TrackerHeartBeatDataSerializer(
                paginated_heart_beat_data, many=True
            )
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateTrackerHeartBeatDataSerializer(data=request.data)
        validate_tracker_heartbeat_data_and_handle_errors(serializer)

        created_heart_beat_data = create_tracker_heart_beat_data(
            timestamp=serializer.validated_data.get("timestamp"),
            latitude=serializer.validated_data["latitude"],
            longitude=serializer.validated_data["longitude"],
            tracker_id=serializer.validated_data["tracker"].id,
        )
        print(created_heart_beat_data)

        serialized_heart_beat_data = TrackerHeartBeatDataSerializer(
            created_heart_beat_data
        )

        return Response(serialized_heart_beat_data.data, status=status.HTTP_201_CREATED)


class DeleteTrackerHeartBeatDataView(APIViewWithPagination):
    def delete(self, request, heartbeat_id):
        delete_tracker_heart_beat_data(heartbeat_id)
        return Response(status=status.HTTP_200_OK)
