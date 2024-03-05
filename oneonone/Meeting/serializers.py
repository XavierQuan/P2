from django.utils import timezone
from rest_framework import serializers
from .models import PendingMeeting, Participant, FinalizedMeeting, TimeSlot
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from Account.serializers import UserSerializer


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ('user', 'response')


class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['meeting', 'user', 'content']

    def create(self, validated_data):
        validated_data['response'] = False  # Automatically set response to False
        if 'content' not in validated_data or not validated_data['content']:
            validated_data['content'] = None  # Set content to NULL if empty
        return Participant.objects.create(**validated_data)


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


class PendingMeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingMeeting
        fields = ['title', 'message', 'deadline', 'time_limit']

    def create(self, validated_data):
        user = self.context['request'].user
        return PendingMeeting.objects.create(owner=user, **validated_data)


class FinalizedMeetingSerializer(serializers.ModelSerializer):
    participant = UserSerializer(read_only=True)

    class Meta:
        model = FinalizedMeeting
        fields = ('title', 'time', 'time_limit', 'participant')


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['meeting', 'start_time', 'priority', 'user']


class TimeSlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['meeting', 'start_time', 'priority', 'user']

    def validate_priority(self, value):
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError("Priority must be an integer.")
