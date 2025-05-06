from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.conf import settings
from django.core.files import File
from elevenlabs import ElevenLabs
import openai
import requests
import os
import time
import logging
import threading
import json
from openai import OpenAI


from .models.generate import Transcription, GeneratedVideo
from .models.Interview import InterviewSession, InterviewResponse
from .serializers import (
    InterviewSessionSerializer,
    InterviewResponseSerializer,
)

logger = logging.getLogger(__name__)


class AudioUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            audio_file = request.FILES.get("audio")
            if not audio_file:
                return Response({"error": "No audio file uploaded"}, status=400)

            transcription = Transcription(audio_file=audio_file)
            transcription.save()

            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            result = client.speech_to_text.convert(
                model_id="scribe_v1", file=audio_file
            )

            transcription.transcript = result.text
            transcription.save()

            return Response(
                {
                    "id": transcription.id,
                    "transcript": transcription.transcript,
                    "created_at": transcription.created_at,
                }
            )
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return Response(
                {"error": "An error occurred while processing the audio."}, status=500
            )


class SpeechToTextView1(APIView):
    base_url = "https://api.heygen.com/"

    def create_video(self, text):
        try:
            url = f"{self.base_url}v2/video/generate"
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "x-api-key": settings.HEYGEN_AI_API_KEY,
            }
            payload = {
                "title": "My Title",
                "video_inputs": [
                    {
                        "character": {
                            "type": "avatar",
                            "avatar_id": "Artur_sitting_office_front",
                            "avatar_style": "normal",
                        },
                        "voice": {
                            "type": "text",
                            "input_text": text,
                            "voice_id": "e5f89518d5564535885cb6d674e57173",
                        },
                    }
                ],
                "test": True,
                "dimension": {"width": 1280, "height": 720},
            }

            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            data = result.get("data")
            return data.get("video_id") if data and "video_id" in data else None
        except Exception as e:
            logger.error(f"Error during video creation: {e}")
            return None

    def get_video_url(self, video_id):
        try:
            url = f"{self.base_url}v1/video_status.get?video_id={video_id}"
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "x-api-key": settings.HEYGEN_AI_API_KEY,
            }

            while True:
                response = requests.get(url, headers=headers)
                data = response.json()
                status = data.get("data", {}).get("status")

                if status == "completed":
                    return data["data"].get("video_url")
                elif status == "failed":
                    return None
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error checking video status: {e}")
            return None

    def download_and_save_video(self, video_url, filename, input_text):
        try:
            response = requests.get(video_url)
            folder_path = "media/heygen_ai_video"
            os.makedirs(folder_path, exist_ok=True)

            full_path = os.path.join(folder_path, f"{filename}.mp4")
            with open(full_path, "wb") as f:
                f.write(response.content)

            with open(full_path, "rb") as f:
                django_file = File(f)
                video_instance = GeneratedVideo.objects.create(
                    video_id=filename, video_file=django_file
                )
            return video_instance
        except Exception as e:
            logger.error(f"Error saving video: {e}")
            return None

    def post(self, request):
        try:
            text = request.data.get("text")
            if not text:
                return Response({"error": "No text provided"}, status=400)

            video_id = self.create_video(text)
            if not video_id:
                return Response({"error": "Failed to create video"}, status=500)

            video_url = self.get_video_url(video_id)
            if not video_url:
                return Response({"error": "Video not ready or failed"}, status=500)

            video_instance = self.download_and_save_video(
                video_url, filename=video_id, input_text=text
            )
            if not video_instance:
                return Response({"error": "Failed to save video"}, status=500)

            return Response(
                {
                    "video_id": video_instance.id,
                    "video_file": video_instance.video_file.url,
                    "created_at": video_instance.created_at,
                }
            )

        except Exception as e:
            logger.error(f"Error during video creation process: {e}")
            return Response(
                {"error": "An error occurred while processing the request."}, status=500
            )


class StartInterviewSessionView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        session = InterviewSession.objects.create(user_id=user_id)
        serializer = InterviewSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadInterviewResponseView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        session_id = request.data.get("session_id")
        question_number = request.data.get("question_number")
        audio_file = request.FILES.get("audio")

        if not all([session_id, question_number, audio_file]):
            return Response(
                {"error": "Missing session_id, question_number, or audio file"},
                status=400,
            )

        try:
            session = InterviewSession.objects.get(id=session_id)
        except InterviewSession.DoesNotExist:
            return Response({"error": "Invalid session ID"}, status=404)

        # Remove any previous response
        InterviewResponse.objects.filter(
            session=session, question_number=question_number
        ).delete()

        # Save initial response
        response = InterviewResponse.objects.create(
            session=session,
            question_number=question_number,
            audio_file=audio_file,
        )

        # Start background task for processing
        def process_audio(response_id, question_number):
            try:
                resp = InterviewResponse.objects.get(id=response_id)

                # Transcription
                elevenlabs_client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
                result = elevenlabs_client.speech_to_text.convert(
                    model_id="scribe_v1", file=resp.audio_file
                )
                resp.transcript = result.text

                # OpenAI analysis
                openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                analysis_prompt = f"""
                    Analyze the following interview response (Question {question_number}) and evaluate the candidate's performance across the following 5 skills:
                    1. Communication
                    2. Critical Thinking
                    3. Confidence
                    4. Adaptability
                    5. Domain Knowledge

                    Return a JSON object with:
                    - A list of 'skills', each with:
                        - 'name' (one of the 5 above),
                        - 'score' (0–100),
                        - 'comment' (short feedback)
                    - An 'overall_summary' string that summarizes their overall performance on this answer.

                    Transcript:
                    \"\"\"{resp.transcript}\"\"\"
                """

                chat_response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an AI interview assistant.",
                        },
                        {"role": "user", "content": analysis_prompt},
                    ],
                )

                # Clean content
                raw_content = chat_response.choices[0].message.content.strip()
                if raw_content.startswith("```json"):
                    raw_content = raw_content.lstrip("```json").rstrip("```").strip()

                parsed_json = json.loads(raw_content)
                resp.analysis_result = parsed_json  # Can be stored as JSONField
                resp.save()

            except Exception as e:
                logger.error(f"[UploadProcessor] Error: {e}")

        threading.Thread(
            target=process_audio, args=(response.id, question_number)
        ).start()

        # Return immediately
        return Response(
            {
                "message": "Answer received. Processing in background.",
                "response_id": response.id,
            },
            status=201,
        )


class InterviewSessionResultView(APIView):
    def get(self, request, session_id):
        try:
            session = InterviewSession.objects.get(id=session_id)
        except InterviewSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)

        responses = session.responses.order_by("question_number")

        # Combine all transcripts for a holistic evaluation
        all_transcripts = "\n\n".join(
            [f"Q{r.question_number}: {r.transcript}" for r in responses if r.transcript]
        )

        if not all_transcripts:
            return Response(
                {"error": "No transcripts found for this session."}, status=400
            )

        # OpenAI summary
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        prompt = f"""
        You are an AI interview evaluator. Based on the following transcript of 10 answers,
        provide an overall evaluation of the candidate.

        Your output must be a JSON object with:
        - A list of 5 'skills' (Communication, Critical Thinking, Confidence, Adaptability, Domain Knowledge)
        - Each skill should have:
            - 'name'
            - 'score' (0–100)
            - 'comment' (short feedback)
        - A single 'overall_summary' that reflects their full performance

        Transcript:
        \"\"\"{all_transcripts}\"\"\"
        """

        chat_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI interview evaluator."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract valid JSON from possibly triple-quoted code block
        raw = chat_response.choices[0].message.content.strip()
        if raw.startswith("```json"):
            raw = raw.lstrip("```json").rstrip("```").strip()

        try:
            result = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"OpenAI JSON parsing failed: {e}")
            return Response({"error": "Failed to parse summary output."}, status=500)

        return Response(
            {
                "session_id": session.id,
                "user_id": session.user_id,
                "summary": result.get("overall_summary"),
                "skills": result.get("skills", []),
            }
        )
