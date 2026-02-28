"use client";

import { FormEvent, useEffect, useState } from "react";
import { Building, createBuilding, listBuildings } from "../lib/api";

export default function Page() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [grossArea, setGrossArea] = useState(1000);
  const [error, setError] = useState("");

  async function reload() {
    try {
      setBuildings(await listBuildings());
      setError("");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    reload();
  }, []);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    try {
      await createBuilding({ name, location, gross_area_m2: grossArea });
      setName("");
      setLocation("");
      setGrossArea(1000);
      await reload();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>FM Building CRUD</h1>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 8, marginBottom: 20 }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="name" required minLength={2} />
        <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="location" required minLength={2} />
        <input
          type="number"
          value={grossArea}
          min={1}
          onChange={(e) => setGrossArea(Number(e.target.value))}
          required
        />
        <button type="submit">Create</button>
      </form>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <ul>
        {buildings.map((building) => (
          <li key={building.id}>
            {building.name} / {building.location} / {building.gross_area_m2} m2
          </li>
        ))}
      </ul>
    </main>
  );
}
