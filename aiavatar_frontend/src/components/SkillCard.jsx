export default function SkillCard({ skill }) {
  return (
    <div className="bg-gray-50 p-4 rounded-xl shadow-sm mb-4">
      <div className="flex justify-between mb-1">
        <h3 className="font-medium text-gray-800">{skill.name}</h3>
        <span className="text-sm font-semibold text-gray-600">
          {skill.score}/100
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
        <div
          className="bg-blue-500 h-2.5 rounded-full transition-all"
          style={{ width: `${skill.score}%` }}
        />
      </div>
      <p className="text-sm text-gray-600">{skill.comment}</p>
    </div>
  );
}
