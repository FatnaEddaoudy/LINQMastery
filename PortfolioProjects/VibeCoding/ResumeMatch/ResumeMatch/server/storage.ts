import { type User, type InsertUser, type Candidate } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  saveCandidateResults(candidates: Candidate[]): Promise<void>;
  getCandidates(): Promise<Candidate[]>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private candidates: Candidate[] = [];

  constructor() {
    this.users = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async saveCandidateResults(candidates: Candidate[]): Promise<void> {
    this.candidates = candidates;
  }

  async getCandidates(): Promise<Candidate[]> {
    return this.candidates;
  }
}

export const storage = new MemStorage();
