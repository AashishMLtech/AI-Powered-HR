"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { API_URL } from "../../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: form.get("email"),
        password: form.get("password")
      })
    });

    if (!response.ok) {
      setError("Invalid email or password");
      return;
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    document.cookie = `hr_token=${data.access_token}; path=/`;
    router.push("/dashboard");
  }

  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark" />
            <strong>AI HR Platform</strong>
          </div>
          <nav className="nav">
            <Link href="/">Home</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </div>
      </header>
      <main className="split">
        <section className="hero-panel">
          <span className="eyebrow">Secure HR access</span>
          <h1>Sign in to the hiring dashboard.</h1>
          <p className="subtle">
            Use the demo account to review jobs, publish approved roles, and inspect candidate screening results.
          </p>
          <div className="hero-card" style={{ marginTop: 20 }}>
            <div className="job-meta">
              <span className="chip">Email: hr@example.com</span>
              <span className="chip">Password: password123</span>
            </div>
            <p className="subtle">
              The interface stays lightweight, but the workflow still feels like a real review system.
            </p>
          </div>
        </section>
        <section className="card">
          <span className="eyebrow">Welcome back</span>
          <h2 className="section-title" style={{ marginTop: 12 }}>HR Login</h2>
          <form className="form" onSubmit={submit}>
            <label>Email<input name="email" type="email" defaultValue="hr@example.com" required /></label>
            <label>Password<input name="password" type="password" defaultValue="password123" required /></label>
            {error && <p className="muted">{error}</p>}
            <button type="submit">Login</button>
          </form>
        </section>
      </main>
    </>
  );
}
