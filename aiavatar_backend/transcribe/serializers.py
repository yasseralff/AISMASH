from rest_framework import serializers
from .models.generate import Transcription, GeneratedVideo
from .models.Interview import  InterviewSession, InterviewResponse
class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'audio_file', 'transcript', 'created_at']


class GeneratedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedVideo
        fields = ['id', 'input_text', 'video_file', 'created_at']

class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = [
            'id',
            'session',
            'question_number',
            'audio_file',
            'transcript',
            'analysis_result',
            'created_at',
        ]
        read_only_fields = ['id', 'transcript', 'analysis_result', 'created_at']


class InterviewSessionSerializer(serializers.ModelSerializer):
    responses = InterviewResponseSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = ['id', 'user_id', 'started_at', 'completed_at', 'responses']
        read_only_fields = ['id', 'started_at', 'completed_at', 'responses']
