from django.urls import path
from .views import (PendingMeetingList,
                    PendingMeetingDetail,
                    FinalizedMeetingList,
                    FinalizedMeetingDetail,
                    PendingMeetingCreateView,
                    TimeSlotCreateView,
                    TimeSlotsListView,
                    ParticipantCreateView,)

urlpatterns = [
    path('pending-meetings/', PendingMeetingList.as_view(), name='pending-meetings'),
    path('pending-meetings/<int:pk>/', PendingMeetingDetail.as_view(), name='pending-meeting-detail'),
    path('finalized-meetings/', FinalizedMeetingList.as_view(), name='finalized-meetings'),
    path('finalized-meetings/<int:pk>/', FinalizedMeetingDetail.as_view(), name='finalized-meeting-detail'),
    path('pending-meetings/create/', PendingMeetingCreateView.as_view(), name='create-pending-meeting'),
    path('time-slots/create/', TimeSlotCreateView.as_view(), name='create-time-slot'),
    path('participants/create/', ParticipantCreateView.as_view(), name='create-participant'),
    path('time-slots/', TimeSlotsListView.as_view(), name='time-slots'),
]
