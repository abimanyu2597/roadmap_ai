import type { RoadmapResponse } from '../lib/types';

type Props = {
  data: RoadmapResponse | null;
};

export function RoadmapView({ data }: Props) {
  if (!data) {
    return (
      <section className="panel result-panel empty-state">
        <div className="section-title">Execution Feed</div>
        <p>Your roadmap will appear here after you run the workflow.</p>
      </section>
    );
  }

  return (
    <section className="panel result-panel">
      <div className="section-title">Execution Feed</div>
      <div className="header-row">
        <div>
          <h2>{data.title}</h2>
          <p>{data.summary}</p>
        </div>
        <div className="score-card">
          <span>Readiness</span>
          <strong>{data.readiness_score}/100</strong>
          <small>{data.execution_mode}</small>
        </div>
      </div>

      <div className="chip-row">
        {data.tools_needed.map((tool) => (
          <span key={tool} className="feature-pill">{tool}</span>
        ))}
      </div>

      <div className="timeline-grid">
        <TimelineCard title="Next 7 Days" items={data.next_7_days} />
        <TimelineCard title="Next 30 Days" items={data.next_30_days} />
        <TimelineCard title="Next 90 Days" items={data.next_90_days} />
      </div>

      <div className="phases">
        {data.phases.map((phase) => (
          <article className="phase-card" key={phase.phase_title}>
            <div className="phase-head">
              <h3>{phase.phase_title}</h3>
              <span>{phase.duration}</span>
            </div>
            <p>{phase.objective}</p>
            <CardList title="Key Tasks" items={phase.key_tasks} />
            <CardList title="Deliverables" items={phase.deliverables} />
            <CardList title="Success Metrics" items={phase.success_metrics} />
            <CardList title="Risks" items={phase.risks} />
          </article>
        ))}
      </div>

      <div className="notes-box">
        <h3>Operator Notes</h3>
        <ul>
          {data.notes.map((note) => (
            <li key={note}>{note}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function TimelineCard({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="timeline-card">
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function CardList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="card-list">
      <strong>{title}</strong>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
