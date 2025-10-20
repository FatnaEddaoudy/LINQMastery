import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import multer from "multer";
import path from "path";
import { promisify } from "util";
import { execFile as execFileCallback } from "child_process";
import fs from "fs";
import { randomUUID } from "crypto";
import OpenAI from "openai";

const execFile = promisify(execFileCallback);

const storage_config = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const ext = path.extname(file.originalname);
    cb(null, file.fieldname + '-' + uniqueSuffix + ext);
  }
});

const upload = multer({
  storage: storage_config,
  fileFilter: (req, file, cb) => {
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
    ];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error("Invalid file type. Only PDF and Word documents are allowed."));
    }
  },
  limits: {
    fileSize: 10 * 1024 * 1024,
  },
});

if (!fs.existsSync("uploads")) {
  fs.mkdirSync("uploads", { recursive: true });
}

const openai = new OpenAI({
  apiKey: process.env.AI_INTEGRATIONS_OPENAI_API_KEY,
  baseURL: process.env.AI_INTEGRATIONS_OPENAI_BASE_URL,
});

export async function registerRoutes(app: Express): Promise<Server> {
  
  // AI-powered skill extraction endpoint
  app.post("/api/extract-skills", async (req, res) => {
    try {
      const { jobDescription } = req.body;
      
      if (!jobDescription || typeof jobDescription !== 'string') {
        return res.status(400).json({ error: "Job description is required" });
      }
      
      const completion = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: `You are an expert HR skill extraction assistant. Extract ALL relevant skills from job descriptions including:
- Hard skills (technical skills, software, tools, methodologies, certifications)
- Soft skills (communication, teamwork, leadership, problem-solving)
- Domain knowledge (industry-specific knowledge)
- Language requirements (Dutch, English, French, etc. with proficiency levels if mentioned)
- Education requirements
- Years of experience requirements

Return ONLY a JSON array of skill strings. Each skill should be clear and specific.
Examples: ["Python", "Machine Learning", "Communication", "Dutch (Native)", "5+ years experience", "Bachelor's Degree in Computer Science"]

Extract skills in the original language they appear (keep Dutch terms in Dutch, French in French, etc.).`
          },
          {
            role: "user",
            content: `Extract all skills from this job description:\n\n${jobDescription}`
          }
        ],
        temperature: 0.3,
        response_format: { type: "json_object" }
      });
      
      const responseContent = completion.choices[0]?.message?.content;
      if (!responseContent) {
        return res.status(500).json({ error: "No response from AI" });
      }
      
      let skillsData;
      try {
        skillsData = JSON.parse(responseContent);
      } catch (parseError) {
        console.error("Failed to parse AI response:", responseContent);
        return res.status(500).json({ error: "Invalid AI response format" });
      }
      
      // Extract skills array from the response (handle different response formats)
      const skills = skillsData.skills || skillsData.extracted_skills || Object.values(skillsData).flat();
      
      if (!Array.isArray(skills)) {
        console.error("Unexpected skills format:", skillsData);
        return res.status(500).json({ error: "Invalid skills format from AI" });
      }
      
      res.json({ skills });
      
    } catch (error: any) {
      console.error("Skill extraction error:", error);
      res.status(500).json({ 
        error: "Failed to extract skills",
        details: error.message 
      });
    }
  });

  app.post("/api/analyze", upload.array("cvFiles", 50), async (req, res) => {
    const files = req.files as Express.Multer.File[];
    
    const cleanupFiles = () => {
      if (files) {
        for (const file of files) {
          fs.unlink(file.path, (err) => {
            if (err) console.error("Error deleting file:", err);
          });
        }
      }
    };

    try {
      const jobDescription = req.body.jobDescription;
      let aiExtractedSkills = req.body.jobSkills; // AI-extracted skills (optional)
      
      // Parse jobSkills if it's a string (from FormData)
      if (typeof aiExtractedSkills === 'string') {
        try {
          aiExtractedSkills = JSON.parse(aiExtractedSkills);
        } catch {
          aiExtractedSkills = [];
        }
      }

      if (!files || files.length === 0) {
        return res.status(400).json({ error: "No CV files uploaded" });
      }

      if (!jobDescription) {
        cleanupFiles();
        return res.status(400).json({ error: "Job description is required" });
      }

      const fileInfo = files.map((file) => ({
        path: file.path,
        originalName: file.originalname
      }));
      
      const fileInfoJson = JSON.stringify(fileInfo);
      const jobSkillsJson = JSON.stringify(aiExtractedSkills || []);
      const args = [jobDescription, fileInfoJson, jobSkillsJson];

      let stdout: string;
      let stderr: string;

      try {
        const result = await execFile("python", ["cv_matcher.py", ...args]);
        stdout = result.stdout;
        stderr = result.stderr;
      } catch (execError: any) {
        console.error("Python execution error:", execError);
        cleanupFiles();
        return res.status(500).json({ 
          error: "Error executing CV analysis",
          details: execError.message 
        });
      }

      if (!stdout || stdout.trim() === "") {
        console.error("Python error:", stderr);
        cleanupFiles();
        return res.status(500).json({ error: "No output from CV analysis" });
      }

      let parsedResponse;
      try {
        parsedResponse = JSON.parse(stdout);
      } catch (parseError) {
        console.error("Failed to parse Python output:", stdout);
        cleanupFiles();
        return res.status(500).json({ error: "Invalid response from CV analysis" });
      }

      const jobSkills = parsedResponse.jobSkills || [];
      const results = parsedResponse.candidates || [];

      const errors: { fileName: string; error: string }[] = [];
      const validCandidates = results
        .map((result: any, index: number) => {
          if (result.error) {
            errors.push({
              fileName: result.fileName || `File ${index + 1}`,
              error: result.error,
            });
            return null;
          }

          return {
            id: randomUUID(),
            jobPostingId: "temp",
            name: result.candidateName || result.fileName.replace(/\.(pdf|docx?|doc)$/i, "").replace(/[-_]/g, " "),
            fileName: result.fileName,
            fileContent: result.fullText || "",
            matchScore: result.matchScore || 0,
            matchedSkills: result.matchedSkills || [],
            analysis: {
              skills: result.skills || [],
              experience: result.experience || "Not specified",
              education: result.education || "Not specified",
              languages: result.languages || [],
            },
            createdAt: new Date().toISOString(),
          };
        })
        .filter((c: any) => c !== null);

      cleanupFiles();

      if (errors.length > 0 && validCandidates.length === 0) {
        return res.status(422).json({
          error: "Failed to process all CVs",
          details: errors,
        });
      }

      await storage.saveCandidateResults(validCandidates);

      res.json({
        success: true,
        jobSkills: jobSkills,
        candidates: validCandidates.sort((a: any, b: any) => (b.matchScore || 0) - (a.matchScore || 0)),
        errors: errors.length > 0 ? errors : undefined,
      });
    } catch (error: any) {
      console.error("Error in analyze route:", error);
      cleanupFiles();
      res.status(500).json({
        error: "Failed to analyze CVs",
        details: error.message,
      });
    }
  });

  app.get("/api/candidates", async (req, res) => {
    try {
      const candidates = await storage.getCandidates();
      res.json(candidates);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch candidates" });
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
