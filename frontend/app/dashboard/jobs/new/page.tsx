"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch, Job } from "../../../../lib/api";

export default function NewJobPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      const job = await apiFetch<Job>("/jobs", {
        method: "POST",
        body: JSON.stringify({
          title: form.get("title"),
          department: form.get("department"),
          location: form.get("location"),
          raw_jd: form.get("raw_jd")
        })
      });
      router.push(`/dashboard/jobs/${job.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create job");
    }
  }

  return (
    <main>
      <div className="toolbar">
        <div>
          <span className="eyebrow">New role</span>
          <h1 className="page-title">Create Job</h1>
          <p className="subtle">Enter raw HR notes and turn them into a polished posting.</p>
        </div>
      </div>

      <section className="card">
        <form className="form" onSubmit={submit}>
          <label>Title<input name="title" required /></label>
          <label>Department<input name="department" /></label>
          <label>Location<input name="location" /></label>
          <label>Raw JD<textarea name="raw_jd" required /></label>
          {error && <p className="muted">{error}</p>}
          <button type="submit">Generate JD</button>
        </form>
      </section>
    </main>
  );
}
