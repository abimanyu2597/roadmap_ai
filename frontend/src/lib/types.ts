export type UserProfile = {
  name?: string;
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  technical_background: boolean;
  budget_range: string;
  timeline_months: number;
  country?: string;
  market?: string;
  team_size: string;
  current_skills: string[];
  constraints: string[];
};

export type RoadmapRequest = {
  goal: string;
  goal_type: string;
  profile: UserProfile;
};

export type Phase = {
  phase_title: string;
  objective: string;
  duration: string;
  key_tasks: string[];
  deliverables: string[];
  success_metrics: string[];
  risks: string[];
};

export type RoadmapResponse = {
  title: string;
  summary: string;
  readiness_score: number;
  execution_mode: string;
  tools_needed: string[];
  next_7_days: string[];
  next_30_days: string[];
  next_90_days: string[];
  phases: Phase[];
  notes: string[];
};
