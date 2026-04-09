import { useState } from 'react';
import { FeatureStrip } from './components/FeatureStrip';
import { Hero } from './components/Hero';
import { RoadmapForm } from './components/RoadmapForm';
import { RoadmapView } from './components/RoadmapView';
import { generateRoadmap } from './lib/api';
import type { RoadmapRequest, RoadmapResponse } from './lib/types';

function App() {
  const [data, setData] = useState<RoadmapResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (payload: RoadmapRequest) => {
    setLoading(true);
    setError(null);
    try {
      const result = await generateRoadmap(payload);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />
      <Hero />
      <FeatureStrip />

      <section className="workspace-grid">
        <RoadmapForm onSubmit={handleSubmit} loading={loading} />
        <RoadmapView data={data} />
      </section>

      {error && <div className="error-toast">{error}</div>}

      <footer className="footer panel">
        <div>
          <strong>RoadPilot AI</strong>
          <p>Neural Command UI · AI Workflow & Roadmap Generator</p>
        </div>
        <div className="creator">
          Created by <strong>Raja Abimanyu N — Data Scientist | AI & Applied Machine Learning</strong>
        </div>
      </footer>
    </main>
  );
}

export default App;
