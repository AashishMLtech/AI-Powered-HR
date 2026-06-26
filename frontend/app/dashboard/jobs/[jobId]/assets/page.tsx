"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "../../../../../lib/api";

type Asset = {
  id: string;
  platform: string;
  caption: string;
  groups: string;
  visual_path: string;
};

export default function AssetsPage({ params }: { params: { jobId: string } }) {
  const [assets, setAssets] = useState<Asset[]>([]);

  useEffect(() => {
    apiFetch<Asset[]>(`/jobs/${params.jobId}/social-assets`).then(setAssets);
  }, []);

  return (
      <main>
      <h1>Social Assets</h1>
      <div className="grid">
        {assets.map((asset) => (
          <section className="card" key={asset.id}>
            <h2>{asset.platform}</h2>
            <p style={{ whiteSpace: "pre-wrap", lineHeight: 1.6 }}>{asset.caption}</p>
            <p className="muted">{asset.groups}</p>
            <button onClick={() => navigator.clipboard.writeText(asset.caption)}>Copy</button>
          </section>
        ))}
      </div>
    </main>
  );
}
