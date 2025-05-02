import { useState } from "react";
import axios from "axios";

export default function SpeechUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("audio", file); // <--- ✅ this is essential

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/transcribe/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(response.data.transcript);
    } catch (error) {
      console.error("Upload Error:", error);
      setResult("Error during upload or transcription.");
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={!file}>
        Upload & Transcribe
      </button>
      <p>Transcription Result: {result}</p>
    </div>
  );
}
