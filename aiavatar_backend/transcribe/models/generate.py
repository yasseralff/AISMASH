from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to="audios/")
    transcript = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at}"
    
class GeneratedVideo(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    video_file = models.FileField(upload_to='heygen_ai_video/')
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_id


