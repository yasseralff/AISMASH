// src/components/SummaryPage.jsx
import React, { useEffect, useState } from 'react';

export default function SummaryPage({ sessionId }) {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetch(`/api/interview/session-result/${sessionId}/`)
      .then((res) => res.json())
      .then((data) => setSummary(data));
  }, [sessionId]);

  if (!summary) return <p className="text-center">Loading summary...</p>;

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h2 className="text-2xl font-bold">Final Interview Summary</h2>
      <p className="bg-gray-100 p-4 rounded shadow whitespace-pre-line">{summary.summary}</p>

      <h3 className="text-xl font-semibold mt-6">All Answers:</h3>
      {summary.responses.map((resp) => (
        <div key={resp.question_number} className="border p-4 rounded shadow mt-4">
          <p className="font-bold">Question {resp.question_number}</p>
          <p><span className="font-semibold">Transcript:</span> {resp.transcript}</p>
          <p><span className="font-semibold">AI Feedback:</span> {resp.analysis_result}</p>
          <audio controls src={resp.audio_file} className="mt-2 w-full" />
        </div>
      ))}
    </div>
  );
}
