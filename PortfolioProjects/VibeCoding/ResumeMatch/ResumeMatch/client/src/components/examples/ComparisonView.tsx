import { ComparisonView } from "../ComparisonView";

const mockComparisons = [
  {
    category: "Technical Skills",
    required: ["React", "TypeScript", "Node.js", "AWS", "Docker"],
    candidate: ["React", "TypeScript", "Node.js", "AWS", "GraphQL", "PostgreSQL"],
  },
  {
    category: "Experience",
    required: ["5+ years development", "Team leadership", "Agile methodology"],
    candidate: ["8 years development", "Led team of 6", "Scrum Master certified"],
  },
  {
    category: "Education",
    required: ["Bachelor's in CS or related field"],
    candidate: ["BS Computer Science, MIT", "AWS Solutions Architect certified"],
  },
];

export default function ComparisonViewExample() {
  return (
    <div className="p-8">
      <ComparisonView
        jobTitle="Senior React Developer"
        candidateName="Sarah Johnson"
        matchScore={92}
        comparisons={mockComparisons}
      />
    </div>
  );
}
