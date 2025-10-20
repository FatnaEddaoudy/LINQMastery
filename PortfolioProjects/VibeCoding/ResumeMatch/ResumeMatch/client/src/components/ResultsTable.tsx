import { useState } from "react";
import { ArrowUpDown, Eye } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface Candidate {
  id: string;
  name: string;
  matchScore: number;
  experience: string;
  education: string;
  skills: string[];
  languages: string[];
}

interface ResultsTableProps {
  candidates: Candidate[];
  onViewDetails?: (id: string) => void;
}

export function ResultsTable({ candidates, onViewDetails }: ResultsTableProps) {
  const [sortField, setSortField] = useState<"name" | "matchScore">("matchScore");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const sortedCandidates = [...candidates].sort((a, b) => {
    const aVal = a[sortField];
    const bVal = b[sortField];
    
    if (typeof aVal === "string" && typeof bVal === "string") {
      return sortOrder === "asc" 
        ? aVal.localeCompare(bVal) 
        : bVal.localeCompare(aVal);
    }
    
    return sortOrder === "asc" ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal);
  });

  const toggleSort = (field: "name" | "matchScore") => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("desc");
    }
  };

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
    <div className="border rounded-md">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[300px]">
              <Button
                variant="ghost"
                onClick={() => toggleSort("name")}
                className="font-semibold -ml-4"
                data-testid="button-sort-name"
              >
                Candidate
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                onClick={() => toggleSort("matchScore")}
                className="font-semibold -ml-4"
                data-testid="button-sort-score"
              >
                Match Score
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>Experience</TableHead>
            <TableHead>Education</TableHead>
            <TableHead>Skills</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedCandidates.map((candidate) => (
            <TableRow key={candidate.id} className="hover-elevate" data-testid={`row-candidate-${candidate.id}`}>
              <TableCell>
                <div className="flex items-center gap-3">
                  <Avatar className="w-10 h-10">
                    <AvatarFallback className="bg-primary text-primary-foreground text-sm font-semibold">
                      {getInitials(candidate.name)}
                    </AvatarFallback>
                  </Avatar>
                  <span className="font-medium text-foreground" data-testid={`text-name-${candidate.id}`}>
                    {candidate.name}
                  </span>
                </div>
              </TableCell>
              <TableCell>
                <Badge className={getScoreColor(candidate.matchScore)} data-testid={`badge-score-${candidate.id}`}>
                  {candidate.matchScore}%
                </Badge>
              </TableCell>
              <TableCell className="text-muted-foreground">{candidate.experience}</TableCell>
              <TableCell className="text-muted-foreground">{candidate.education}</TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {candidate.skills.slice(0, 3).map((skill, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                  {candidate.skills.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{candidate.skills.length - 3}
                    </Badge>
                  )}
                </div>
              </TableCell>
              <TableCell className="text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onViewDetails?.(candidate.id)}
                  data-testid={`button-view-${candidate.id}`}
                >
                  <Eye className="w-4 h-4 mr-2" />
                  View
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
