from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    AudioUploadView,
    SpeechToTextView1,
    StartInterviewSessionView,
    UploadInterviewResponseView,
    InterviewSessionResultView,  
)

urlpatterns = [
    path("transcribe/", AudioUploadView.as_view(), name="transcribe_audio"),
    path("speech-to-text/", SpeechToTextView1.as_view(), name="speech_to_text"),
    path("interview/start/", StartInterviewSessionView.as_view(), name="start_interview"),
    path("interview/upload-response/", UploadInterviewResponseView.as_view(), name="upload_interview_response"),
    path("interview/session-result/<int:session_id>/", InterviewSessionResultView.as_view(), name="interview_session_result"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
