// src/components/AudioRecorder.jsx
import React, { useState, useRef } from 'react';

export default function AudioRecorder({ onRecorded }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (e) => {
      audioChunksRef.current.push(e.data);
    };

    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      onRecorded(blob);
    };

    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div className="mt-4">
      {!recording ? (
        <button onClick={startRecording} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Start Recording
        </button>
      ) : (
        <button onClick={stopRecording} className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
          Stop Recording
        </button>
      )}
    </div>
  );
}
