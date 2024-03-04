from django.utils import timezone
from rest_framework import serializers
from .models import PendingMeeting, Participant, FinalizedMeeting
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from Account.serializers import UserSerializer


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ('user', 'response')


class PendingMeetingSerializer(serializers.ModelSerializer):
    has_passed_deadline = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = PendingMeeting
        fields = ('id', 'title', 'deadline', 'has_passed_deadline', 'participants')

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_has_passed_deadline(self, obj):
        return obj.deadline < timezone.now()

    @extend_schema_field(serializers.ListField(child=ParticipantSerializer()))
    def get_participants(self, obj):
        participants = Participant.objects.filter(meeting=obj)
        return ParticipantSerializer(participants, many=True).data


class PendingMeetingDetailSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = PendingMeeting
        fields = '__all__'

    @extend_schema_field(serializers.ListField(child=ParticipantSerializer()))
    def get_participants(self, obj):
        participants = Participant.objects.filter(meeting=obj)
        return ParticipantSerializer(participants, many=True).data


class FinalizedMeetingSerializer(serializers.ModelSerializer):
    participant = UserSerializer(read_only=True)

    class Meta:
        model = FinalizedMeeting
        fields = ('title', 'time', 'time_limit', 'participant')
