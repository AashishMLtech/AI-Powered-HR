const API_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export type Job = {
  id: string;
  title: string;
  department: string;
  location: string;
  raw_jd: string;
  ai_jd: string;
  status: string;
  created_at: string;
};

export type Candidate = {
  candidate_id: string;
  application_id: string;
  full_name: string;
  email: string;
  github_url: string;
  linkedin_url: string;
  combined_score: number;
  cv_score: number;
  github_score: number;
  linkedin_score: number | null;
  ai_resume_flag: number;
  status: string;
};

export function getToken() {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("token") || "";
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json();
}

export { API_URL };
