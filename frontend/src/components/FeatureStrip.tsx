const features = [
  'LangGraph workflow orchestration',
  'Founder profile-aware roadmap generation',
  'Readiness scoring and milestone planning',
  'Neural Command futuristic SaaS UI',
  'Creator branding built in'
];

export function FeatureStrip() {
  return (
    <section className="feature-strip">
      {features.map((feature) => (
        <div key={feature} className="feature-pill">{feature}</div>
      ))}
    </section>
  );
}
