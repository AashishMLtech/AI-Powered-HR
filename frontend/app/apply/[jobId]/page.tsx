"use client";

import { FormEvent, useEffect, useState } from "react";
import { API_URL, Job } from "../../../lib/api";

export default function ApplyPage({ params }: { params: { jobId: string } }) {
  const [job, setJob] = useState<Job | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/jobs/${params.jobId}/public`).then((response) => response.json()).then(setJob);
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    const form = new FormData(event.currentTarget);
    form.set("job_id", params.jobId);
    form.set("consent_given", form.get("consent_given") ? "true" : "false");

    const response = await fetch(`${API_URL}/applications`, {
      method: "POST",
      body: form
    });

    setMessage(response.ok ? "Application submitted" : await response.text());
  }

  if (!job) return <main><p>Loading...</p></main>;

  return (
    <main>
      <div className="toolbar">
        <div>
          <span className="eyebrow">Public application</span>
          <h1 className="page-title">{job.title}</h1>
          <p className="subtle">{job.department} · {job.location}</p>
        </div>
      </div>
      <div className="split">
        <section className="card">
          <h2 className="section-title">Role Overview</h2>
          <pre>{job.ai_jd}</pre>
        </section>
        <section className="card">
          <h2 className="section-title">Apply</h2>
          <form className="form" onSubmit={submit}>
            <label>Full name<input name="full_name" required /></label>
            <label>Email<input name="email" type="email" required /></label>
            <label>Phone<input name="phone" /></label>
            <label>GitHub URL<input name="github_url" /></label>
            <label>LinkedIn URL<input name="linkedin_url" /></label>
            <label>Resume PDF or DOCX<input name="resume" type="file" accept=".pdf,.docx" required /></label>
            <label className="row"><input name="consent_given" type="checkbox" required /> I consent to resume screening for this application.</label>
            <button type="submit">Submit Application</button>
            {message && <p className="muted">{message}</p>}
          </form>
        </section>
      </div>
    </main>
  );
}
