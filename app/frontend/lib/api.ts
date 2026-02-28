const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export type Building = {
  id: number;
  name: string;
  location: string;
  gross_area_m2: number;
};

const defaultHeaders = { "X-Role": "admin", "Content-Type": "application/json" };

export async function listBuildings(): Promise<Building[]> {
  const response = await fetch(`${API_BASE}/api/v1/buildings`, { headers: { "X-Role": "viewer" }, cache: "no-store" });
  if (!response.ok) throw new Error("建物一覧の取得に失敗しました");
  return response.json();
}

export async function createBuilding(payload: Omit<Building, "id">): Promise<void> {
  const response = await fetch(`${API_BASE}/api/v1/buildings`, {
    method: "POST",
    headers: defaultHeaders,
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("建物作成に失敗しました");
}
