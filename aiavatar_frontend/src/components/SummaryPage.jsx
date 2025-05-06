import React, { useEffect, useState } from "react";
import SummaryCard from "./SummaryCard";
import SkillsList from "./SkillsList";

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
      <h2 className="text-2xl font-bold dark:text-gray-300">
        Final Interview Summary
      </h2>

      <SummaryCard summary={summary.summary} />
      <SkillsList skills={summary.skills} />
    </div>
  );
}
