import { useState } from 'react';
import type { RoadmapRequest } from '../lib/types';

const initialState: RoadmapRequest = {
  goal: 'I want to launch an AI SaaS that helps recruiters screen candidates faster.',
  goal_type: 'ai_saas',
  profile: {
    name: 'Founder',
    experience_level: 'intermediate',
    technical_background: true,
    budget_range: 'medium',
    timeline_months: 6,
    country: 'India',
    market: 'Recruitment tech',
    team_size: 'solo',
    current_skills: ['Python', 'FastAPI', 'LLMs'],
    constraints: ['Part-time founder', 'Lean budget'],
  },
};

type Props = {
  onSubmit: (payload: RoadmapRequest) => Promise<void>;
  loading: boolean;
};

export function RoadmapForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<RoadmapRequest>(initialState);

  return (
    <section className="panel form-panel">
      <div className="section-title">Mission Intake Console</div>
      <div className="field-grid">
        <label>
          Goal
          <textarea
            rows={4}
            value={form.goal}
            onChange={(e) => setForm({ ...form, goal: e.target.value })}
          />
        </label>
        <label>
          Goal Type
          <select
            value={form.goal_type}
            onChange={(e) => setForm({ ...form, goal_type: e.target.value })}
          >
            <option value="ai_saas">AI SaaS</option>
            <option value="ai_business">AI Business</option>
            <option value="general">General</option>
          </select>
        </label>
        <label>
          Founder Name
          <input
            value={form.profile.name}
            onChange={(e) => setForm({ ...form, profile: { ...form.profile, name: e.target.value } })}
          />
        </label>
        <label>
          Experience Level
          <select
            value={form.profile.experience_level}
            onChange={(e) =>
              setForm({
                ...form,
                profile: { ...form.profile, experience_level: e.target.value as RoadmapRequest['profile']['experience_level'] },
              })
            }
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </label>
        <label>
          Budget
          <input
            value={form.profile.budget_range}
            onChange={(e) => setForm({ ...form, profile: { ...form.profile, budget_range: e.target.value } })}
          />
        </label>
        <label>
          Timeline (months)
          <input
            type="number"
            min={1}
            max={24}
            value={form.profile.timeline_months}
            onChange={(e) => setForm({ ...form, profile: { ...form.profile, timeline_months: Number(e.target.value) } })}
          />
        </label>
        <label>
          Market
          <input
            value={form.profile.market}
            onChange={(e) => setForm({ ...form, profile: { ...form.profile, market: e.target.value } })}
          />
        </label>
        <label>
          Team Size
          <input
            value={form.profile.team_size}
            onChange={(e) => setForm({ ...form, profile: { ...form.profile, team_size: e.target.value } })}
          />
        </label>
        <label className="wide">
          Current Skills (comma separated)
          <input
            value={form.profile.current_skills.join(', ')}
            onChange={(e) =>
              setForm({
                ...form,
                profile: {
                  ...form.profile,
                  current_skills: e.target.value.split(',').map((item) => item.trim()).filter(Boolean),
                },
              })
            }
          />
        </label>
        <label className="wide">
          Constraints (comma separated)
          <input
            value={form.profile.constraints.join(', ')}
            onChange={(e) =>
              setForm({
                ...form,
                profile: {
                  ...form.profile,
                  constraints: e.target.value.split(',').map((item) => item.trim()).filter(Boolean),
                },
              })
            }
          />
        </label>
      </div>
      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={form.profile.technical_background}
          onChange={(e) =>
            setForm({
              ...form,
              profile: { ...form.profile, technical_background: e.target.checked },
            })
          }
        />
        Technical founder
      </label>
      <button className="primary-btn" onClick={() => void onSubmit(form)} disabled={loading}>
        {loading ? 'Generating Neural Roadmap...' : 'Generate Roadmap'}
      </button>
    </section>
  );
}
