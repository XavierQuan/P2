from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PendingMeeting, FinalizedMeeting
from .serializers import (PendingMeetingSerializer,
                          PendingMeetingDetailSerializer,
                          FinalizedMeetingSerializer,
                          PendingMeetingCreateSerializer,
                          TimeSlotCreateSerializer,
                          ParticipantCreateSerializer,)
from drf_spectacular.utils import extend_schema


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


class PendingMeetingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Create Pending Meeting',
        description='Allows the creation of a new pending meeting.',
        request=PendingMeetingCreateSerializer,
        responses={201: PendingMeetingCreateSerializer},
    )
    def post(self, request, format=None):
        serializer = PendingMeetingCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            meeting = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Create Time Slot',
        description='Create a new time slot for a pending meeting.',
        request=TimeSlotCreateSerializer,
        responses={201: TimeSlotCreateSerializer},
    )
    def post(self, request, format=None):
        serializer = TimeSlotCreateSerializer(data=request.data)
        if serializer.is_valid():
            time_slot = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipantCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Add Participant to Meeting',
        description='Add a new participant to a pending meeting.',
        request=ParticipantCreateSerializer,
        responses={201: ParticipantCreateSerializer},
    )
    def post(self, request, format=None):
        serializer = ParticipantCreateSerializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

