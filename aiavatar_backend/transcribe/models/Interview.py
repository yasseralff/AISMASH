from django.db import models

class InterviewSession(models.Model):
    user_id = models.CharField(max_length=255)  # Or use ForeignKey to User model if you're using auth
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} for User {self.user_id}"


class InterviewResponse(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='responses')
    question_number = models.PositiveIntegerField()
    audio_file = models.FileField(upload_to='responses/')
    transcript = models.TextField(blank=True)
    analysis_result = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'question_number')
        ordering = ['question_number']

    def __str__(self):
        return f"Q{self.question_number} Response for Session {self.session.id}"
