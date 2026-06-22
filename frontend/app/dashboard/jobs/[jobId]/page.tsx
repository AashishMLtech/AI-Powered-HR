"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch, Job } from "../../../../lib/api";

export default function JobDetailPage({ params }: { params: { jobId: string } }) {
  const [job, setJob] = useState<Job | null>(null);
  const [message, setMessage] = useState("");

  async function load() {
    setJob(await apiFetch<Job>(`/jobs/${params.jobId}`));
  }

  useEffect(() => {
    load();
  }, []);

  async function saveAiJd() {
    if (!job) return;
    const saved = await apiFetch<Job>(`/jobs/${job.id}`, {
      method: "PATCH",
      body: JSON.stringify({ ai_jd: job.ai_jd })
    });
    setJob(saved);
    setMessage("Saved");
  }

  async function action(path: string) {
    const saved = await apiFetch<Job>(path, { method: path.includes("regenerate") ? "POST" : "PATCH" });
    setJob(saved);
    setMessage("Updated");
  }

  if (!job) return <main><p>Loading...</p></main>;

  return (
    <main>
      <div className="toolbar">
        <div>
          <span className="eyebrow">Job review</span>
          <h1 className="page-title">{job.title}</h1>
          <p className="subtle">{job.department} - {job.location}</p>
        </div>
        <span className="badge">{job.status}</span>
      </div>
      <div className="split">
        <section className="card">
          <h2 className="section-title">AI Job Description</h2>
          <label>
            <textarea value={job.ai_jd} onChange={(event) => setJob({ ...job, ai_jd: event.target.value })} />
          </label>
          <div className="row">
            <button onClick={saveAiJd}>Save Draft</button>
            <button onClick={() => action(`/jobs/${job.id}/approve`)}>Approve</button>
            <button className="danger" onClick={() => action(`/jobs/${job.id}/reject`)}>Reject</button>
            <button className="secondary" onClick={() => action(`/jobs/${job.id}/regenerate`)}>Regenerate</button>
          </div>
          <div className="row" style={{ marginTop: 10 }}>
            <Link className="button secondary" href={`/dashboard/jobs/${job.id}/assets`}>Social assets</Link>
            <Link className="button secondary" href={`/dashboard/jobs/${job.id}/candidates`}>Candidates</Link>
          </div>
          {message && <p className="muted">{message}</p>}
        </section>
        <aside className="hero-side">
          <div className="hero-card">
            <span className="eyebrow">Workflow</span>
            <p className="subtle" style={{ marginTop: 12 }}>
              Edit the description, approve when ready, and publish the role to the public application page.
            </p>
          </div>
          <div className="hero-card">
            <span className="eyebrow">Status</span>
            <p className="subtle" style={{ marginTop: 12 }}>
              Approved jobs unlock candidate applications and social asset generation.
            </p>
          </div>
        </aside>
      </div>
    </main>
  );
}
