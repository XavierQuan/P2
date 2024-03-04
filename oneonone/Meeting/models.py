from django.db import models
from ..Account.models import User


class PendingMeeting(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_limit = models.DateTimeField()
    message = models.TextField()
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()


class TimeSlot(models.Model):
    meeting = models.ForeignKey(PendingMeeting, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    priority = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Participant(models.Model):
    meeting = models.ForeignKey(PendingMeeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.BooleanField()
    content = models.TextField()


class FinalizedMeeting(models.Model):
    meeting = models.OneToOneField(PendingMeeting, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time = models.DateTimeField()
    time_limit = models.DateTimeField()
    participants = models.ManyToManyField(User)


class SuggestedSchedule(models.Model):
    meeting = models.ForeignKey(PendingMeeting, on_delete=models.CASCADE)


class SuggestedTimeSlot(models.Model):
    meeting = models.ForeignKey(SuggestedSchedule, on_delete=models.CASCADE)
    time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
