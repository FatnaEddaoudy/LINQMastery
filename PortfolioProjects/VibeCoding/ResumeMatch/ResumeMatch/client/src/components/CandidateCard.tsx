import { User, Briefcase, GraduationCap } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface CandidateCardProps {
  id: string;
  name: string;
  matchScore: number;
  experience?: string;
  education?: string;
  skills: string[];
  onViewDetails?: () => void;
}

export function CandidateCard({
  id,
  name,
  matchScore,
  experience,
  education,
  skills,
  onViewDetails,
}: CandidateCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-chart-2 text-white";
    if (score >= 60) return "bg-chart-4 text-white";
    return "bg-muted text-muted-foreground";
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <Card className="hover-elevate" data-testid={`card-candidate-${id}`}>
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <Avatar className="w-12 h-12">
              <AvatarFallback className="bg-primary text-primary-foreground font-semibold">
                {getInitials(name)}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-foreground" data-testid={`text-name-${id}`}>
                {name}
              </h3>
              {experience && (
                <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                  <Briefcase className="w-3 h-3" />
                  {experience}
                </p>
              )}
            </div>
          </div>
          <div className="text-right">
            <div
              className={`text-2xl font-bold px-3 py-1 rounded-md ${getScoreColor(matchScore)}`}
              data-testid={`text-score-${id}`}
            >
              {matchScore}%
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {education && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <GraduationCap className="w-4 h-4" />
            <span>{education}</span>
          </div>
        )}
        <div>
          <p className="text-sm font-medium text-foreground mb-2">Key Skills</p>
          <div className="flex flex-wrap gap-2">
            {skills.slice(0, 6).map((skill, index) => (
              <Badge key={index} variant="secondary" data-testid={`badge-skill-${id}-${index}`}>
                {skill}
              </Badge>
            ))}
            {skills.length > 6 && (
              <Badge variant="outline">+{skills.length - 6} more</Badge>
            )}
          </div>
        </div>
        <Button
          variant="outline"
          className="w-full"
          onClick={onViewDetails}
          data-testid={`button-view-details-${id}`}
        >
          View Full Comparison
        </Button>
      </CardContent>
    </Card>
  );
}
