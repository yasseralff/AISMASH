import React, { useState } from "react";
import AudioRecorder from "./AudioRecorder";

export default function QuestionStep({ question, sessionId, onComplete }) {
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("question_number", question.id);
    formData.append("audio", recordedBlob, `answer_q${question.id}.webm`);

    setIsUploading(true);
    const res = await fetch("/api/interview/upload-response/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setIsUploading(false);
    onComplete(data); // 👈 This moves to the next question
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <video
        src={question.videoUrl}
        controls
        autoPlay
        className="w-full max-w-4xl rounded-lg shadow"
      />

      <AudioRecorder onRecorded={(blob) => setRecordedBlob(blob)} />

      <div className="flex gap-4">
        <button
          onClick={handleUpload}
          disabled={!recordedBlob || isUploading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Submit Answer
        </button>

        <button
          onClick={() => setRecordedBlob(null)}
          className="bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400"
        >
          Repeat Question
        </button>
      </div>
    </div>
  );
}
