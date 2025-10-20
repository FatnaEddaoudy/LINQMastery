import { JobDescriptionInput } from "../JobDescriptionInput";

export default function JobDescriptionInputExample() {
  return (
    <div className="p-8 max-w-3xl mx-auto">
      <JobDescriptionInput
        onChange={(value) => console.log("Job description:", value)}
      />
    </div>
  );
}
