import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <strong>AI HR Platform</strong>
          <nav className="nav">
            <Link href="/login">Login</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </div>
      </header>
      <main>
        <section className="card">
          <h1>Hiring workflow dashboard</h1>
          <p className="muted">
            Create jobs, review AI-written job descriptions, generate social assets, and screen candidates.
          </p>
          <Link className="button" href="/login">HR Login</Link>
        </section>
      </main>
    </>
  );
}
