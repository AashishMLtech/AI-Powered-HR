"use client";

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
    <main>
      <section className="card">
        <h1>HR Login</h1>
        <form className="form" onSubmit={submit}>
          <label>Email<input name="email" type="email" defaultValue="hr@example.com" required /></label>
          <label>Password<input name="password" type="password" defaultValue="password123" required /></label>
          {error && <p className="muted">{error}</p>}
          <button type="submit">Login</button>
        </form>
      </section>
    </main>
  );
}
