// App.tsx
// Main app component: handles login, and once logged in, shows the list of calendars.

import { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

// Shape of a calendar object, matching our backend's Calendar model
type Calendar = {
  id: number;
  user_id: number;
  name: string;
  color: string;
};

// Decodes the payload of a JWT token without verifying its signature.
// This is safe here because we only use it to read the user_id for display —
// the backend is the one that actually verifies the token on every request.
function decodeToken(token: string): { user_id: number } | null {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Try to load an existing token from localStorage when the app first loads
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem("token")
  );

  const [calendars, setCalendars] = useState<Calendar[]>([]);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Incorrect email or password");
      }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
    setCalendars([]);
  }

  // useEffect runs code in response to something changing — here, whenever
  // "token" changes, we fetch the user's calendars.
  useEffect(() => {
    if (!token) return;

    const decoded = decodeToken(token);
    if (!decoded) return;

    async function fetchCalendars() {
      const response = await fetch(
        `${API_URL}/users/${decoded!.user_id}/calendars`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setCalendars(data);
      }
    }

    fetchCalendars();
  }, [token]);

  // ---------- Logged in view ----------
  if (token) {
    return (
      <div style={{ padding: "2rem", maxWidth: "400px", margin: "0 auto" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <h1>My Calendars</h1>
          <button onClick={handleLogout}>Log out</button>
        </div>

        {calendars.length === 0 && <p>No calendars yet.</p>}

        <ul style={{ listStyle: "none", padding: 0 }}>
          {calendars.map((cal) => (
            <li
              key={cal.id}
              style={{
                padding: "0.75rem",
                marginBottom: "0.5rem",
                borderLeft: `6px solid ${cal.color}`,
                background: "#222",
                borderRadius: "4px",
              }}
            >
              {cal.name}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  // ---------- Login form view ----------
  return (
    <div style={{ padding: "2rem", maxWidth: "300px", margin: "0 auto" }}>
      <h1>Study Planner</h1>
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "1rem" }}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ display: "block", width: "100%" }}
            required
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ display: "block", width: "100%" }}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Log in</button>
      </form>
    </div>
  );
}

export default App;