from django.db import models
from rental.vehicle.models import Vehicle

class Tracker(models.Model):
    name = models.CharField(max_length=255)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='tracker')
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tracker'
        verbose_name_plural = 'Trackers'
        ordering = ['created_date']


class TrackerHeartBeatData(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, related_name='heartbeat_data')

    class Meta:
        verbose_name = 'Tracker Heart Beat Data'
        verbose_name_plural = 'Tracker Heart Beat Data'
        ordering = ['-timestamp']
