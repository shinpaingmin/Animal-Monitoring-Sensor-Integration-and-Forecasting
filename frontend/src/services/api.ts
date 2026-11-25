import type { CaseCreate, CaseRecord, HealthStatus } from "../types/contracts";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null) as { detail?: string } | null;
    throw new Error(detail?.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthStatus>("/health"),
  listCases: () => request<CaseRecord[]>("/cases"),
  createCase: (payload: CaseCreate) => request<CaseRecord>("/cases", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
};
