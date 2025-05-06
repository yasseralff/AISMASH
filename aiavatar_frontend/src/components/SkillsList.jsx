import SkillCard from "./SkillCard";

export default function SkillsList({ skills }) {
  return (
    <div className="p-6 bg-white rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Skill Breakdown</h2>
      {skills.map((skill, index) => (
        <SkillCard key={index} skill={skill} />
      ))}
    </div>
  );
}
