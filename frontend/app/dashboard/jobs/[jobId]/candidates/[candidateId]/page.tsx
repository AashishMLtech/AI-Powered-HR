"use client";

import { FormEvent, useEffect, useState } from "react";
import { apiFetch } from "../../../../../../lib/api";

type ScreeningData = {
  candidate: { full_name: string; email: string; github_url: string; linkedin_url: string };
  screening: {
    cv_score: number;
    github_score: number;
    linkedin_score: number | null;
    combined_score: number;
    ai_resume_flag: number;
    reasoning: string;
    details: Record<string, unknown>;
  };
};

export default function CandidateDetailPage({ params }: { params: { candidateId: string } }) {
  const [data, setData] = useState<ScreeningData | null>(null);

  async function load() {
    setData(await apiFetch<ScreeningData>(`/candidates/${params.candidateId}/screening`));
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await apiFetch(`/candidates/${params.candidateId}/linkedin-check`, {
      method: "PATCH",
      body: JSON.stringify({
        linkedin_score: Number(form.get("linkedin_score")),
        notes: form.get("notes")
      })
    });
    await load();
  }

  if (!data) return <main><p>Loading...</p></main>;

  return (
    <main>
      <section className="card">
        <h1>{data.candidate.full_name}</h1>
        <p className="muted">{data.candidate.email}</p>
        <p>Combined score: <strong>{data.screening.combined_score}</strong></p>
        <p>CV: {data.screening.cv_score} · GitHub: {data.screening.github_score} · LinkedIn: {data.screening.linkedin_score ?? "not checked"}</p>
        <p>AI resume flag: {data.screening.ai_resume_flag} advisory only</p>
        <pre>{data.screening.reasoning}</pre>
      </section>

      <section className="card">
        <h2>LinkedIn Manual Check</h2>
        <form className="form" onSubmit={submit}>
          <label>LinkedIn score<input name="linkedin_score" type="number" min="0" max="100" required /></label>
          <label>Notes<textarea name="notes" /></label>
          <button type="submit">Save LinkedIn Check</button>
        </form>
      </section>
    </main>
  );
}
