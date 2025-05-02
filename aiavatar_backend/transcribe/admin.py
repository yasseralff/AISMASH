from django.contrib import admin
from .models.generate import Transcription, GeneratedVideo
from .models.Interview import InterviewSession, InterviewResponse


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "audio_file", "transcript", "created_at")
    search_fields = ("transcript",)
    readonly_fields = ("created_at",)


@admin.register(GeneratedVideo)
class GeneratedVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "video_id", "video_file", "created_at")
    search_fields = ("video_id",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "started_at", "completed_at")
    search_fields = ("user_id",)
    readonly_fields = ("started_at", "completed_at")


@admin.register(InterviewResponse)
class InterviewResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "question_number", "audio_file", "transcript", "created_at")
    search_fields = ("transcript", "analysis_result")
    readonly_fields = ("created_at", "transcript", "analysis_result")
