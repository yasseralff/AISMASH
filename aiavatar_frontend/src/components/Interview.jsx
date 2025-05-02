// src/components/Interview.jsx
import React, { useState } from 'react';
import QuestionStep from './QuestionStep';
import SummaryPage from './SummaryPage';

const QUESTIONS = [
  { id: 1, videoUrl: '/videos/q1.mp4' },
  { id: 2, videoUrl: '/videos/q2.mp4' },
  // Add up to 10...
];

export default function Interview({ sessionId }) {
  const [step, setStep] = useState(0);
  const [showSummary, setShowSummary] = useState(false);

  const handleNext = () => {
    if (step < QUESTIONS.length - 1) {
      setStep(step + 1);
    } else {
      setShowSummary(true);
    }
  };

  if (showSummary) {
    return <SummaryPage sessionId={sessionId} />;
  }

  return (
    <QuestionStep
      question={QUESTIONS[step]}
      sessionId={sessionId}
      onComplete={handleNext}
    />
  );
}
