import Link from "next/link";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <strong>AI HR Platform</strong>
          <nav className="nav">
            <Link href="/dashboard">Jobs</Link>
            <Link href="/dashboard/jobs/new">New Job</Link>
          </nav>
        </div>
      </header>
      {children}
    </>
  );
}
