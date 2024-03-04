from django.urls import path
from .views import PendingMeetingList, PendingMeetingDetail, FinalizedMeetingList, FinalizedMeetingDetail

urlpatterns = [
    path('pending-meetings/', PendingMeetingList.as_view(), name='pending-meetings'),
    path('pending-meetings/<int:pk>/', PendingMeetingDetail.as_view(), name='pending-meeting-detail'),
    path('finalized-meetings/', FinalizedMeetingList.as_view(), name='finalized-meetings'),
    path('finalized-meetings/<int:pk>/', FinalizedMeetingDetail.as_view(), name='finalized-meeting-detail'),
]
