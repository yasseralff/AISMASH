import { useState } from "react";
import axios from "axios";

export default function TextUpload() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  const handleUpload = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/speech-to-text/",
        { text }, // JSON body
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setResult("http://localhost:8000" + response.data.video_path);
      console.log("http://localhost:8000" + response.data.video_path);
    } catch (error) {
      console.error("Upload Error:", error);
      setResult("Error during video generation.");
    }
  };

  return (
    <div>
      <textarea
        placeholder="Enter text to turn into avatar video"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={5}
      />
      <button onClick={handleUpload} disabled={!text}>
        Generate Avatar Video
      </button>
      {result && (
        <div>
          <p>Video generated at:</p>
          <video controls width="500">
            <source src={result} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}
