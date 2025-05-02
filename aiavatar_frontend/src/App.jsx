import React, { useState } from 'react';
import Interview from './components/Interview';

export default function App() {
  const [sessionId, setSessionId] = useState(null);

  const startInterview = async () => {
    try {
      const res = await fetch('/api/interview/start/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: 'zakky001' }),
      });

      if (!res.ok) {
        throw new Error('Failed to start interview');
      }

      const data = await res.json();
      console.log('Session started:', data);  // ✅ Add this line for debug
      setSessionId(data.id);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to start interview. See console for details.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">
        AI Interview App
      </h1>

      {!sessionId ? (
        <button
          onClick={startInterview}
          className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700"
        >
          Start Interview
        </button>
      ) : (
        <Interview sessionId={sessionId} />
      )}
    </div>
  );
}
