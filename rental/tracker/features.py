from rental.tracker.models import Tracker, TrackerHeartBeatData
from settings.utils.exceptions import NotFound404APIException


def get_trackers():
    trackers = Tracker.objects.all()
    return trackers


def get_tracker(tracker_id: str):
    try:
        tracker = Tracker.objects.get(id=tracker_id)
    except Tracker.DoesNotExist:
        raise NotFound404APIException(f"Tracker with id {tracker_id} not found")

    return tracker


def create_tracker(name: str, vehicle: str):
    new_tracker = Tracker.objects.create(name=name, vehicle=vehicle)
    new_tracker.save()
    return new_tracker


def update_tracker(tracker_id: str, name: str = None, vehicle: str = None):
    try:
        tracker = Tracker.objects.get(id=tracker_id)
    except Tracker.DoesNotExist:
        raise NotFound404APIException(f"Tracker with id {tracker_id} not found")

    if name:
        tracker.name = name
    if vehicle:
        tracker.vehicle = vehicle

    tracker.full_clean()
    tracker.save()
    return tracker


def delete_tracker(tracker_id):
    try:
        tracker = Tracker.objects.get(id=tracker_id)
        tracker.delete()
    except Tracker.DoesNotExist:
        raise NotFound404APIException(f"Tracker with id {tracker_id} not found")


def get_tracker_heart_beat_data():
    heart_beat_data = TrackerHeartBeatData.objects.all()
    return heart_beat_data


def get_tracker_heart_beat_data_by_tracker_id(tracker_id: str):
    try:
        heart_beat_data = TrackerHeartBeatData.objects.filter(tracker_id=tracker_id)
    except TrackerHeartBeatData.DoesNotExist:
        raise NotFound404APIException(
            f"Tracker heart beat data for tracker with id {tracker_id} not found"
        )

    return heart_beat_data


def create_tracker_heart_beat_data(
    timestamp: str, latitude: float, longitude: float, tracker_id: str
):
    try:
        tracker = Tracker.objects.get(id=tracker_id)
    except TrackerHeartBeatData.DoesNotExist:
        raise NotFound404APIException(f"Tracker with id {tracker_id} not found")

    new_heart_beat_data = TrackerHeartBeatData.objects.create(
        latitude=latitude,
        longitude=longitude,
        tracker=tracker,
        timestamp=timestamp,
    )
    return new_heart_beat_data


def delete_tracker_heart_beat_data(heartbeat_id):
    try:
        heart_beat_data = TrackerHeartBeatData.objects.filter(id=heartbeat_id)
        heart_beat_data.delete()
    except TrackerHeartBeatData.DoesNotExist:
        raise NotFound404APIException(
            f"Tracker HeartBeatData with id {heartbeat_id} not found"
        )
