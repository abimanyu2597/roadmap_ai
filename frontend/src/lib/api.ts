import type { RoadmapRequest, RoadmapResponse } from './types';

const API_BASE = 'http://localhost:8000/api/v1';

export async function generateRoadmap(payload: RoadmapRequest): Promise<RoadmapResponse> {
  const response = await fetch(`${API_BASE}/roadmap/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to generate roadmap. Check backend logs or API config.');
  }

  return response.json();
}
