"use client";

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
      <div className="row">
        <h1>Jobs</h1>
        <Link className="button" href="/dashboard/jobs/new">Create Job</Link>
      </div>
      {error && <p className="muted">{error}</p>}
      <div className="grid">
        {jobs.map((job) => (
          <section className="card" key={job.id}>
            <h2>{job.title}</h2>
            <p className="muted">{job.department || "General"} · {job.location || "Remote"}</p>
            <span className="badge">{job.status}</span>
            <div className="row">
              <Link href={`/dashboard/jobs/${job.id}`}>Review</Link>
              <Link href={`/dashboard/jobs/${job.id}/assets`}>Assets</Link>
              <Link href={`/dashboard/jobs/${job.id}/candidates`}>Candidates</Link>
              <Link href={`/apply/${job.id}`}>Apply page</Link>
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
