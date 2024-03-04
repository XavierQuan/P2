from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PendingMeeting, FinalizedMeeting
from .serializers import PendingMeetingSerializer, PendingMeetingDetailSerializer, FinalizedMeetingSerializer
from drf_spectacular.utils import extend_schema, extend_schema_field


class PendingMeetingList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Pending Meetings',
        description='Retrieve a list of all pending meetings filtered by the owner.',
        responses={200: PendingMeetingSerializer(many=True)},
    )
    def get(self, request, format=None):
        meetings = PendingMeeting.objects.filter(owner=request.user)
        serializer = PendingMeetingSerializer(meetings, many=True)
        return Response(serializer.data)


class PendingMeetingDetail(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Pending Meeting Details',
        description='Retrieve detailed information about a specific pending meeting.',
        responses={200: PendingMeetingDetailSerializer},
    )
    def get(self, request, pk, format=None):
        meeting = PendingMeeting.objects.get(pk=pk)
        serializer = PendingMeetingDetailSerializer(meeting)
        return Response(serializer.data)


class FinalizedMeetingList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Finalized Meetings',
        description='Retrieve a list of finalized (scheduled) meetings filtered by the meeting owner.',
        responses={200: FinalizedMeetingSerializer(many=True)},
    )
    def get(self, request, format=None):
        meetings = FinalizedMeeting.objects.filter(meeting__owner=request.user)
        serializer = FinalizedMeetingSerializer(meetings, many=True)
        return Response(serializer.data)


class FinalizedMeetingDetail(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Finalized Meeting Details',
        description='Retrieve detailed information about a specific finalized (scheduled) meeting.',
        responses={200: FinalizedMeetingSerializer},
    )
    def get(self, request, pk, format=None):
        try:
            meeting = FinalizedMeeting.objects.get(pk=pk, meeting__owner=request.user)
            serializer = FinalizedMeetingSerializer(meeting)
            return Response(serializer.data)
        except FinalizedMeeting.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

