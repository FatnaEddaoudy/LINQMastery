import { useState } from "react";
import { FileUploadZone } from "@/components/FileUploadZone";
import { JobDescriptionInput } from "@/components/JobDescriptionInput";
import { CandidateCard } from "@/components/CandidateCard";
import { ResultsTable } from "@/components/ResultsTable";
import { ComparisonView } from "@/components/ComparisonView";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Download, LayoutGrid, Table as TableIcon, X, Sparkles } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useToast } from "@/hooks/use-toast";

interface Candidate {
  id: string;
  name: string;
  fileName: string;
  matchScore: number;
  matchedSkills: string[];
  analysis: {
    skills: string[];
    experience: string;
    education: string;
    languages: string[];
  };
}

export default function HomePage() {
  const [step, setStep] = useState<"upload" | "results" | "comparison">("upload");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");
  const [selectedCandidate, setSelectedCandidate] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState("");
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [jobSkills, setJobSkills] = useState<string[]>([]);
  const { toast } = useToast();

  const handleFilesChange = (files: File[]) => {
    setUploadedFiles(files);
  };

  const handleJobDescriptionChange = (value: string) => {
    setJobDescription(value);
  };

  const handleAnalyze = async () => {
    if (uploadedFiles.length === 0) {
      toast({
        title: "No CVs uploaded",
        description: "Please upload at least one CV file to analyze",
        variant: "destructive",
      });
      return;
    }

    if (!jobDescription.trim()) {
      toast({
        title: "Job description required",
        description: "Please enter a job description to match against",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setProgress(0);

    const progressInterval = setInterval(() => {
      setProgress((prev) => Math.min(prev + 5, 80));
    }, 300);

    try {
      // Step 1: Extract skills using AI
      setProgress(10);
      const skillsResponse = await fetch("/api/extract-skills", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ jobDescription }),
      });

      if (!skillsResponse.ok) {
        const error = await skillsResponse.json();
        console.error("Skill extraction failed:", error);
        // Continue without AI skills - will fall back to NLP extraction
      }

      let extractedSkills: string[] = [];
      try {
        const skillsData = await skillsResponse.json();
        extractedSkills = skillsData.skills || [];
        setProgress(30);
      } catch {
        // Continue without AI skills
        setProgress(30);
      }

      // Step 2: Analyze CVs with extracted skills
      const formData = new FormData();
      formData.append("jobDescription", jobDescription);
      formData.append("jobSkills", JSON.stringify(extractedSkills));
      
      uploadedFiles.forEach((file) => {
        formData.append("cvFiles", file);
      });

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Failed to analyze CVs");
      }

      const data = await response.json();
      setProgress(100);
      setCandidates(data.candidates);
      
      // Ensure jobSkills is always an array
      let skills = data.jobSkills || [];
      if (typeof skills === 'string') {
        try {
          skills = JSON.parse(skills);
        } catch {
          skills = [];
        }
      }
      setJobSkills(Array.isArray(skills) ? skills : []);
      
      setTimeout(() => {
        setIsProcessing(false);
        setStep("results");
        toast({
          title: "Analysis complete",
          description: `Successfully analyzed ${data.candidates.length} candidates`,
        });
      }, 500);
    } catch (error: any) {
      clearInterval(progressInterval);
      setIsProcessing(false);
      setProgress(0);
      toast({
        title: "Analysis failed",
        description: error.message || "An error occurred while analyzing CVs",
        variant: "destructive",
      });
    }
  };

  const handleViewDetails = (id: string) => {
    setSelectedCandidate(id);
    setStep("comparison");
  };

  const handleBack = () => {
    if (step === "comparison") {
      setStep("results");
      setSelectedCandidate(null);
    } else {
      setStep("upload");
    }
  };

  const handleClearCVs = () => {
    setUploadedFiles([]);
    toast({
      title: "CVs cleared",
      description: "All uploaded CVs have been removed",
    });
  };

  const handleClearDescription = () => {
    setJobDescription("");
    toast({
      title: "Description cleared",
      description: "Job description has been removed",
    });
  };

  const formatCandidatesForTable = () => {
    return candidates.map((candidate) => ({
      id: candidate.id,
      name: candidate.name,
      matchScore: candidate.matchScore,
      experience: candidate.analysis.experience,
      education: candidate.analysis.education,
      skills: candidate.analysis.skills,
      languages: candidate.analysis.languages || [],
    }));
  };

  const extractLanguagesFromJobDescription = (text: string): string[] => {
    const languagesMap: Record<string, string> = {
      'dutch': 'Dutch',
      'nederlands': 'Dutch',
      'french': 'French',
      'frans': 'French',
      'english': 'English',
      'engels': 'English',
      'german': 'German',
      'duits': 'German',
      'spanish': 'Spanish',
      'spaans': 'Spanish',
    };

    const found: string[] = [];
    const textLower = text.toLowerCase();

    for (const [key, lang] of Object.entries(languagesMap)) {
      if (textLower.includes(key) && !found.includes(lang)) {
        found.push(lang);
      }
    }

    return found;
  };

  const getComparisonData = () => {
    const candidate = candidates.find((c) => c.id === selectedCandidate);
    if (!candidate) return [];

    // Ensure jobSkills is always an array
    const skillsRequired = Array.isArray(jobSkills) ? jobSkills : [];

    return [
      {
        category: "Technical Skills",
        required: skillsRequired.length > 0 ? skillsRequired : ["Skills as per job description"],
        candidate: candidate.analysis.skills || [],
      },
      {
        category: "Experience",
        required: [jobDescription.match(/\d+\+?\s*years?/i)?.[0] || "Experience required"],
        candidate: [candidate.analysis.experience || "Not specified"],
      },
      {
        category: "Education",
        required: [jobDescription.match(/(Bachelor|Master|PhD|BS|MS|MBA|degree)/i)?.[0] || "Degree required"],
        candidate: [candidate.analysis.education || "Not specified"],
      },
      {
        category: "Languages",
        required: extractLanguagesFromJobDescription(jobDescription),
        candidate: candidate.analysis.languages || [],
      },
    ];
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b sticky top-0 bg-background z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            {step !== "upload" && (
              <Button
                variant="ghost"
                size="icon"
                onClick={handleBack}
                data-testid="button-back"
              >
                <ArrowLeft className="w-5 h-5" />
              </Button>
            )}
            <h1 className="text-2xl font-bold text-foreground" data-testid="text-app-title">
              HR CV Matcher
            </h1>
          </div>
          <div className="flex items-center gap-2">
            {step === "results" && (
              <Button variant="outline" data-testid="button-export">
                <Download className="w-4 h-4 mr-2" />
                Export Results
              </Button>
            )}
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {step === "upload" && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-2">
                Compare Job Description with CVs
              </h2>
              <p className="text-muted-foreground">
                Upload candidate CVs and enter the job description to get AI-powered matching results
              </p>
            </div>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <CardTitle>Step 1: Upload CVs</CardTitle>
                {uploadedFiles.length > 0 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleClearCVs}
                    disabled={isProcessing}
                    data-testid="button-clear-cvs"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Clear CVs
                  </Button>
                )}
              </CardHeader>
              <CardContent>
                <FileUploadZone files={uploadedFiles} onFilesChange={handleFilesChange} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <CardTitle>Step 2: Job Description</CardTitle>
                {jobDescription.trim() && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleClearDescription}
                    disabled={isProcessing}
                    data-testid="button-clear-description"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Clear Description
                  </Button>
                )}
              </CardHeader>
              <CardContent>
                <JobDescriptionInput value={jobDescription} onChange={handleJobDescriptionChange} />
              </CardContent>
            </Card>

            <div className="flex justify-end">
              <Button
                size="lg"
                onClick={handleAnalyze}
                disabled={isProcessing || uploadedFiles.length === 0 || !jobDescription.trim()}
                data-testid="button-analyze"
              >
                {isProcessing ? "Analyzing..." : "Analyze & Match"}
              </Button>
            </div>

            {isProcessing && (
              <Card>
                <CardContent className="pt-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-foreground">
                        Processing CVs and matching with job description...
                      </p>
                      <p className="text-sm text-muted-foreground">{progress}%</p>
                    </div>
                    <Progress value={progress} data-testid="progress-analysis" />
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {step === "results" && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold text-foreground mb-2">
                  Matching Results
                </h2>
                <p className="text-muted-foreground">
                  {candidates.length} candidates analyzed and ranked by match score
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant={viewMode === "grid" ? "secondary" : "ghost"}
                  size="icon"
                  onClick={() => setViewMode("grid")}
                  data-testid="button-view-grid"
                >
                  <LayoutGrid className="w-4 h-4" />
                </Button>
                <Button
                  variant={viewMode === "table" ? "secondary" : "ghost"}
                  size="icon"
                  onClick={() => setViewMode("table")}
                  data-testid="button-view-table"
                >
                  <TableIcon className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {Array.isArray(jobSkills) && jobSkills.length > 0 && (
              <Card>
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-primary" />
                    <CardTitle className="text-lg">AI Extracted Skills ({jobSkills.length})</CardTitle>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    These skills were extracted from your job description and used for matching
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {jobSkills.map((skill, index) => (
                      <Badge key={index} variant="secondary" data-testid={`badge-extracted-skill-${index}`}>
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {candidates.length === 0 ? (
              <Card>
                <CardContent className="pt-6 text-center text-muted-foreground">
                  No candidates found. Please try again.
                </CardContent>
              </Card>
            ) : viewMode === "grid" ? (
              <div className="grid md:grid-cols-2 gap-6">
                {candidates.map((candidate) => (
                  <CandidateCard
                    key={candidate.id}
                    id={candidate.id}
                    name={candidate.name}
                    matchScore={candidate.matchScore}
                    experience={candidate.analysis.experience}
                    education={candidate.analysis.education}
                    skills={candidate.analysis.skills}
                    onViewDetails={() => handleViewDetails(candidate.id)}
                  />
                ))}
              </div>
            ) : (
              <ResultsTable
                candidates={formatCandidatesForTable()}
                onViewDetails={handleViewDetails}
              />
            )}
          </div>
        )}

        {step === "comparison" && selectedCandidate && (
          <ComparisonView
            jobTitle="Job Position"
            candidateName={candidates.find((c) => c.id === selectedCandidate)?.name || ""}
            matchScore={candidates.find((c) => c.id === selectedCandidate)?.matchScore || 0}
            comparisons={getComparisonData()}
          />
        )}
      </main>
    </div>
  );
}
