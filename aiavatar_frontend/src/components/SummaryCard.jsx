export default function SummaryCard({ summary }) {
  return (
    <div className="p-6 bg-white rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-2">Overall Summary</h2>
      <p className="text-gray-700 whitespace-pre-line">{summary}</p>
    </div>
  );
}
