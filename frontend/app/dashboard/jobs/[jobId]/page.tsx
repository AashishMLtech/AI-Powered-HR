"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
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
      <section className="card">
        <div className="row">
          <h1>{job.title}</h1>
          <span className="badge">{job.status}</span>
        </div>
        <p className="muted">{job.department} · {job.location}</p>
        <label>
          AI Job Description
          <textarea value={job.ai_jd} onChange={(event) => setJob({ ...job, ai_jd: event.target.value })} />
        </label>
        <div className="row">
          <button onClick={saveAiJd}>Save</button>
          <button onClick={() => action(`/jobs/${job.id}/approve`)}>Approve</button>
          <button className="danger" onClick={() => action(`/jobs/${job.id}/reject`)}>Reject</button>
          <button className="secondary" onClick={() => action(`/jobs/${job.id}/regenerate`)}>Regenerate</button>
          <Link href={`/dashboard/jobs/${job.id}/assets`}>Social assets</Link>
          <Link href={`/dashboard/jobs/${job.id}/candidates`}>Candidates</Link>
        </div>
        {message && <p className="muted">{message}</p>}
      </section>
    </main>
  );
}
