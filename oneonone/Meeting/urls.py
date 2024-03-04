from django.urls import path
from .views import PendingMeetingList, PendingMeetingDetail, ScheduledMeetingList

urlpatterns = [
    path('pending-meetings/', PendingMeetingList.as_view(), name='pending-meetings'),
    path('pending-meetings/<int:pk>/', PendingMeetingDetail.as_view(), name='pending-meeting-detail'),
    path('scheduled-meetings/', ScheduledMeetingList.as_view(), name='scheduled-meetings'),
]
