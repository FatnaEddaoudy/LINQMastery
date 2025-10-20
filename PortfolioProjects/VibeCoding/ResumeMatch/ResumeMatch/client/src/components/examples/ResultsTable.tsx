import { ResultsTable } from "../ResultsTable";

const mockCandidates = [
  {
    id: "1",
    name: "Sarah Johnson",
    matchScore: 92,
    experience: "8 years",
    education: "BS Computer Science",
    skills: ["React", "TypeScript", "Node.js", "AWS"],
  },
  {
    id: "2",
    name: "Michael Chen",
    matchScore: 85,
    experience: "6 years",
    education: "MS Software Engineering",
    skills: ["React", "JavaScript", "Python", "Docker"],
  },
  {
    id: "3",
    name: "Emily Rodriguez",
    matchScore: 78,
    experience: "5 years",
    education: "BS Information Systems",
    skills: ["Angular", "TypeScript", "Node.js", "MongoDB"],
  },
];

export default function ResultsTableExample() {
  return (
    <div className="p-8">
      <ResultsTable
        candidates={mockCandidates}
        onViewDetails={(id) => console.log("View details:", id)}
      />
    </div>
  );
}
