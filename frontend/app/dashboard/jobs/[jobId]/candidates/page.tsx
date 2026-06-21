"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch, Candidate } from "../../../../../lib/api";

export default function CandidatesPage({ params }: { params: { jobId: string } }) {
  const [candidates, setCandidates] = useState<Candidate[]>([]);

  useEffect(() => {
    apiFetch<Candidate[]>(`/jobs/${params.jobId}/candidates`).then(setCandidates);
  }, []);

  return (
    <main>
      <h1>Candidates</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Scores</th>
            <th>Advisory AI Flag</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((candidate) => (
            <tr key={candidate.candidate_id}>
              <td>
                <strong>{candidate.full_name}</strong>
                <br />
                <span className="muted">{candidate.email}</span>
              </td>
              <td>
                Combined {candidate.combined_score} · CV {candidate.cv_score} · GitHub {candidate.github_score}
              </td>
              <td>{candidate.ai_resume_flag}</td>
              <td><Link href={`/dashboard/jobs/${params.jobId}/candidates/${candidate.candidate_id}`}>Open</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
