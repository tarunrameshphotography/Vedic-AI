import {
  ApiError,
  type ApiErrorDetail,
  type BirthInput,
  type CaseManifest,
  type ConsultResult,
  type DeferredRegistry,
  type RuleCardRaw,
} from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(0, `could not reach the API at ${BASE_URL} -- is the backend running?`);
  }

  if (!response.ok) {
    let detail: ApiErrorDetail | string = `request failed with status ${response.status}`;
    try {
      const body = await response.json();
      // FastAPI's own pydantic-validation shape (`detail: [...]`) differs
      // from the app's own error shape (`detail: {error_type, message}`) --
      // both are rendered, neither is paraphrased into something friendlier.
      if (body && typeof body.detail === "object" && !Array.isArray(body.detail)) {
        detail = body.detail as ApiErrorDetail;
      } else if (body && Array.isArray(body.detail)) {
        detail = body.detail
          .map((e: { loc?: unknown[]; msg?: string }) => `${(e.loc ?? []).join(".")}: ${e.msg ?? ""}`)
          .join("; ");
      } else if (body && typeof body.detail === "string") {
        detail = body.detail;
      }
    } catch {
      // response body was not JSON; fall through with the generic message
    }
    throw new ApiError(response.status, detail);
  }

  return response.json() as Promise<T>;
}

export function health(): Promise<{ status: string; engine_version: string; card_count: number }> {
  return request("/health");
}

export function consult(birth: BirthInput): Promise<ConsultResult> {
  return request("/consult", { method: "POST", body: JSON.stringify(birth) });
}

export function getCard(cardId: string): Promise<RuleCardRaw> {
  return request(`/cards/${encodeURIComponent(cardId)}`);
}

export function getDeferred(): Promise<DeferredRegistry> {
  return request("/deferred");
}

export function listCases(): Promise<CaseManifest[]> {
  return request("/cases");
}

export function getCase(slug: string): Promise<CaseManifest> {
  return request(`/cases/${encodeURIComponent(slug)}`);
}

export function saveCase(label: string, notes: string, birth: BirthInput): Promise<CaseManifest> {
  return request("/cases", { method: "POST", body: JSON.stringify({ label, notes, birth }) });
}
