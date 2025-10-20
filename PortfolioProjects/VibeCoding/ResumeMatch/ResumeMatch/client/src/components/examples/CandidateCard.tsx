import { CandidateCard } from "../CandidateCard";

export default function CandidateCardExample() {
  return (
    <div className="p-8 max-w-md mx-auto">
      <CandidateCard
        id="1"
        name="Sarah Johnson"
        matchScore={92}
        experience="8 years in Software Development"
        education="BS Computer Science, MIT"
        skills={["React", "TypeScript", "Node.js", "AWS", "GraphQL", "Docker", "CI/CD", "Agile"]}
        onViewDetails={() => console.log("View details clicked")}
      />
    </div>
  );
}
