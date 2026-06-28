"use client";

export const dynamic = "force-dynamic";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch, Job } from "../../lib/api";

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch<Job[]>("/jobs").then(setJobs).catch((err) => setError(err.message));
  }, []);

  return (
    <main>
      <div className="toolbar">
        <div>
          <span className="eyebrow">HR workspace</span>
          <h1 className="page-title">Jobs</h1>
          <p className="subtle">Review open roles, status, and candidate activity from one dashboard.</p>
        </div>
        <Link className="button" href="/dashboard/jobs/new">Create Job</Link>
      </div>

      {error && <p className="muted">{error}</p>}

      <div className="grid">
        {jobs.length === 0 && (
          <div className="empty-state">No jobs yet. Create your first role to start the workflow.</div>
        )}
        {jobs.map((job) => (
          <section className="card" key={job.id}>
            <div className="job-title">
              <div>
                <h2 className="section-title" style={{ marginBottom: 6 }}>{job.title}</h2>
                <p className="muted">{job.department || "General"} - {job.location || "Remote"}</p>
              </div>
              <span className={`badge ${job.status === "published" ? "" : "status-muted"}`}>{job.status}</span>
            </div>
            <div className="job-meta">
              <span className="chip">Review</span>
              <span className="chip">Assets</span>
              <span className="chip">Candidates</span>
            </div>
            <div className="row">
              <Link className="button secondary" href={`/dashboard/jobs/${job.id}`}>Open</Link>
              <Link className="button secondary" href={`/dashboard/jobs/${job.id}/assets`}>Assets</Link>
              <Link className="button secondary" href={`/dashboard/jobs/${job.id}/candidates`}>Candidates</Link>
              <Link className="button secondary" href={`/apply/${job.id}`}>Public Apply</Link>
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
