import { useState, useEffect } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";

interface JobDescriptionInputProps {
  value?: string;
  onChange?: (value: string) => void;
  extractedSkills?: string[];
}

export function JobDescriptionInput({ value = "", onChange, extractedSkills = [] }: JobDescriptionInputProps) {
  const [description, setDescription] = useState(value);

  useEffect(() => {
    setDescription(value);
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDescription(e.target.value);
    onChange?.(e.target.value);
  };

  return (
    <div className="space-y-4">
      <div>
        <Label htmlFor="job-description" className="text-base font-semibold">
          Job Description
        </Label>
        <p className="text-sm text-muted-foreground mt-1">
          Enter the job requirements, skills, and qualifications you're looking for
        </p>
      </div>
      <Textarea
        id="job-description"
        value={description}
        onChange={handleChange}
        placeholder="E.g., Looking for a Senior React Developer with 5+ years of experience in building scalable web applications. Must have expertise in TypeScript, Redux, and RESTful APIs..."
        className="min-h-48 resize-none"
        data-testid="textarea-job-description"
      />
      <div className="flex items-center justify-between">
        <p className="text-xs text-muted-foreground" data-testid="text-char-count">
          {description.length} characters
        </p>
      </div>
      
      {extractedSkills.length > 0 && (
        <div className="space-y-2 pt-2 border-t">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-primary" />
            <Label className="text-sm font-semibold">AI Extracted Skills ({extractedSkills.length})</Label>
          </div>
          <div className="flex flex-wrap gap-2">
            {extractedSkills.map((skill, index) => (
              <Badge key={index} variant="secondary" data-testid={`badge-skill-${index}`}>
                {skill}
              </Badge>
            ))}
          </div>
          <p className="text-xs text-muted-foreground">
            These skills will be used to match candidates
          </p>
        </div>
      )}
    </div>
  );
}
