import { CheckCircle2, Circle, XCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ComparisonItem {
  category: string;
  required: string[];
  candidate: string[];
}

interface ComparisonViewProps {
  jobTitle: string;
  candidateName: string;
  matchScore: number;
  comparisons: ComparisonItem[];
}

export function ComparisonView({
  jobTitle,
  candidateName,
  matchScore,
  comparisons,
}: ComparisonViewProps) {
  const getMatchStatus = (required: string, candidateSkills: string[]) => {
    if (!Array.isArray(candidateSkills)) return "none";
    const normalized = candidateSkills.map((s) => s.toLowerCase());
    if (normalized.includes(required.toLowerCase())) {
      return "full";
    }
    if (normalized.some((s) => s.includes(required.toLowerCase()) || required.toLowerCase().includes(s))) {
      return "partial";
    }
    return "none";
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-chart-2 text-white";
    if (score >= 60) return "bg-chart-4 text-white";
    return "bg-muted text-muted-foreground";
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground" data-testid="text-comparison-title">
            {candidateName} vs {jobTitle}
          </h2>
          <p className="text-muted-foreground mt-1">
            Detailed qualification comparison
          </p>
        </div>
        <div className={`text-3xl font-bold px-4 py-2 rounded-md ${getScoreColor(matchScore)}`} data-testid="text-comparison-score">
          {matchScore}%
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="sticky top-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg">Job Requirements</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {comparisons.map((comp, index) => {
              const requiredItems = Array.isArray(comp.required) ? comp.required : [];
              const candidateItems = Array.isArray(comp.candidate) ? comp.candidate : [];
              
              return (
                <div key={index}>
                  <h4 className="font-semibold text-foreground mb-3">{comp.category}</h4>
                  <div className="space-y-2">
                    {requiredItems.map((req, reqIndex) => {
                      const status = getMatchStatus(req, candidateItems);
                      return (
                        <div
                          key={reqIndex}
                          className="flex items-center gap-2 text-sm"
                          data-testid={`requirement-${index}-${reqIndex}`}
                        >
                          {status === "full" && (
                            <CheckCircle2 className="w-4 h-4 text-chart-2 flex-shrink-0" />
                          )}
                          {status === "partial" && (
                            <Circle className="w-4 h-4 text-chart-4 flex-shrink-0" />
                          )}
                          {status === "none" && (
                            <XCircle className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                          )}
                          <span className={status === "none" ? "text-muted-foreground" : "text-foreground"}>
                            {req}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-4">
            <CardTitle className="text-lg">Candidate Qualifications</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {comparisons.map((comp, index) => {
              const requiredItems = Array.isArray(comp.required) ? comp.required : [];
              const candidateItems = Array.isArray(comp.candidate) ? comp.candidate : [];
              
              return (
                <div key={index}>
                  <h4 className="font-semibold text-foreground mb-3">{comp.category}</h4>
                  {comp.category === "Technical Skills" ? (
                    <div className="flex flex-wrap gap-2">
                      {candidateItems.map((skill, skillIndex) => {
                        const isMatched = requiredItems.some(
                          (req) => req.toLowerCase() === skill.toLowerCase() ||
                                   req.toLowerCase().includes(skill.toLowerCase()) ||
                                   skill.toLowerCase().includes(req.toLowerCase())
                        );
                        return (
                          <Badge
                            key={skillIndex}
                            variant={isMatched ? "default" : "secondary"}
                            className={isMatched ? "bg-chart-2" : ""}
                            data-testid={`skill-${index}-${skillIndex}`}
                          >
                            {skill}
                          </Badge>
                        );
                      })}
                    </div>
                  ) : (
                    <div className="space-y-1">
                      {candidateItems.map((item, itemIndex) => (
                        <p key={itemIndex} className="text-foreground" data-testid={`item-${index}-${itemIndex}`}>
                          {item}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Legend</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-6">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-chart-2" />
            <span className="text-sm text-muted-foreground">Full Match</span>
          </div>
          <div className="flex items-center gap-2">
            <Circle className="w-4 h-4 text-chart-4" />
            <span className="text-sm text-muted-foreground">Partial Match</span>
          </div>
          <div className="flex items-center gap-2">
            <XCircle className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">No Match</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
