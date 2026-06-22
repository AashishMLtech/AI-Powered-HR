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
          <h1>Hiring workflow, presented with clarity.</h1>
          <p className="subtle">
            Create jobs, review AI-written descriptions, publish assets, and screen candidates from one calm dashboard.
          </p>
          <div className="hero-actions">
            <Link className="button" href="/login">Open HR Login</Link>
            <Link className="button secondary" href="/dashboard">View Dashboard</Link>
          </div>
        </section>
        <aside className="hero-side">
          <div className="metric">
            <strong>Jobs</strong>
            <span>Approve and publish roles quickly.</span>
          </div>
          <div className="metric">
            <strong>Candidates</strong>
            <span>Compare resumes and screening output.</span>
          </div>
          <div className="metric">
            <strong>Assets</strong>
            <span>Keep job promotion materials organized.</span>
          </div>
        </aside>
      </main>
    </>
  );
}
