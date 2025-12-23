"use client";

import { useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Status = "idle" | "loading" | "done" | "error";

type GenerateInvoicesButtonProps = {
  runId: string;
};

export function GenerateInvoicesButton({ runId }: GenerateInvoicesButtonProps) {
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState<string | null>(null);

  const handleClick = async () => {
    if (!runId) {
      return;
    }
    setStatus("loading");
    setMessage(null);
    try {
      const response = await fetch(
        `${API_BASE}/invoices/${encodeURIComponent(runId)}`,
        { method: "POST" }
      );
      if (!response.ok) {
        throw new Error(`Invoice API error ${response.status}`);
      }
      const data = (await response.json()) as { invoices?: Array<unknown> };
      const count = Array.isArray(data.invoices) ? data.invoices.length : 0;
      setStatus("done");
      setMessage(`Ready: ${count}`);
    } catch (error) {
      setStatus("error");
      setMessage("Failed");
    }
  };

  const label =
    status === "loading" ? "Generating..." : "Generate invoices";

  return (
    <div className="dropzone__actions">
      <button
        className="button secondary"
        type="button"
        onClick={handleClick}
        disabled={status === "loading"}
      >
        {label}
      </button>
      {message ? <span className="chip">{message}</span> : null}
    </div>
  );
}
