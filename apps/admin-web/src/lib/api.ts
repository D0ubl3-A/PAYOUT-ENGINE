export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || process.env.API_BASE_URL || "http://localhost:8000";

async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getUploads() {
  return apiGet<{ uploads: Array<Record<string, unknown>> }>("/uploads");
}

export async function getExtractions() {
  return apiGet<{ extractions: Array<Record<string, unknown>> }>("/extractions");
}

export async function getRuns() {
  return apiGet<{ runs: Array<Record<string, unknown>> }>("/payouts/runs");
}

export async function getInvoices(runId?: string) {
  const query = runId ? `?run_id=${encodeURIComponent(runId)}` : "";
  return apiGet<{ invoices: Array<Record<string, unknown>> }>(`/invoices${query}`);
}
