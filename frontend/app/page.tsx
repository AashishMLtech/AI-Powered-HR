import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark" />
            <strong>AI HR Platform</strong>
          </div>
          <nav className="nav">
            <Link href="/login">Login</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </div>
      </header>
      <main className="hero">
        <section className="hero-panel">
          <span className="eyebrow">HR automation platform</span>
          <h1>Hiring workflow, presented with clarity and momentum.</h1>
          <p className="subtle">
            Create jobs, review AI-written descriptions, publish assets, and screen candidates from one polished dashboard built for modern recruiting teams.
          </p>
          <div className="hero-actions">
            <Link className="button" href="/login">Open HR Login</Link>
            <Link className="button secondary" href="/dashboard">View Dashboard</Link>
          </div>
          <div className="hero-card" style={{ marginTop: 20 }}>
            <div className="job-meta">
              <span className="chip">Role review</span>
              <span className="chip">Candidate scoring</span>
              <span className="chip">Social assets</span>
            </div>
            <p className="subtle">
              Built to help HR teams move quickly without losing visibility into approvals, applications, and candidate quality.
            </p>
          </div>
        </section>
        <aside className="hero-side">
          <div className="metric">
            <strong>Jobs</strong>
            <span>Approve and publish roles with a cleaner review flow.</span>
          </div>
          <div className="metric">
            <strong>Candidates</strong>
            <span>Compare resumes, scores, and notes in one place.</span>
          </div>
          <div className="metric">
            <strong>Assets</strong>
            <span>Generate platform-specific promotion copy that stays on brand.</span>
          </div>
        </aside>
      </main>
    </>
  );
}
