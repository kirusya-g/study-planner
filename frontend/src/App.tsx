// App.tsx
// This is the main component of our app. Right now it only contains
// a simple login form that talks to our FastAPI backend.

import { useState } from "react";
import "./App.css";

// The address where our backend is running
const API_URL = "http://127.0.0.1:8000";

function App() {
  // useState creates a piece of state — a value that React remembers
  // between renders, and that triggers a re-render when it changes.
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // This function runs when the user submits the login form
  async function handleLogin(e: React.FormEvent) {
    e.preventDefault(); // stop the browser from reloading the page on submit

    setError(null);

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Incorrect email or password");
      }

      const data = await response.json();
      setToken(data.access_token);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  // If we already have a token, show a simple "logged in" message
  if (token) {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>You are logged in!</h1>
        <p style={{ wordBreak: "break-all" }}>Token: {token}</p>
      </div>
    );
  }

  // Otherwise, show the login form
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