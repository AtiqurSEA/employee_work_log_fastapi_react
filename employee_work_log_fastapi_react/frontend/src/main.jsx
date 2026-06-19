import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { apiRequest } from "./api";
import "./style.css";

const emptyLog = {
  date: "",
  task: "",
  hours: "",
  status: "Pending",
  project: "",
  comments: "",
};

function App() {
  const [user, setUser] = useState(null);
  const [logs, setLogs] = useState([]);
  const [view, setView] = useState("login");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [logForm, setLogForm] = useState(emptyLog);
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    checkCurrentUser();
  }, []);

  async function checkCurrentUser() {
    try {
      const currentUser = await apiRequest("/api/auth/me");
      setUser(currentUser);
      setView("dashboard");
      loadLogs();
    } catch {
      setUser(null);
      setView("login");
    }
  }

  async function loadLogs() {
    try {
      const data = await apiRequest("/api/worklogs");
      setLogs(data);
    } catch (err) {
      setError(err.message);
    }
  }

  function updateForm(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function updateLogForm(event) {
    setLogForm({ ...logForm, [event.target.name]: event.target.value });
  }

  function showMessage(text) {
    setMessage(text);
    setError("");
  }

  function showError(text) {
    setError(text);
    setMessage("");
  }

  async function register(event) {
    event.preventDefault();
    try {
      await apiRequest("/api/auth/register", {
        method: "POST",
        body: JSON.stringify(form),
      });
      setForm({ full_name: "", email: "", password: "" });
      setView("login");
      showMessage("Account created successfully. Please log in.");
    } catch (err) {
      showError(err.message);
    }
  }

  async function login(event) {
    event.preventDefault();
    try {
      const loggedInUser = await apiRequest("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email: form.email, password: form.password }),
      });
      setUser(loggedInUser);
      setForm({ full_name: "", email: "", password: "" });
      setView("dashboard");
      showMessage("Logged in successfully.");
      await loadLogs();
    } catch (err) {
      showError(err.message);
    }
  }

  async function logout() {
    await apiRequest("/api/auth/logout", { method: "POST" });
    setUser(null);
    setLogs([]);
    setView("login");
    showMessage("Logged out successfully.");
  }

  async function submitLog(event) {
    event.preventDefault();
    try {
      const payload = { ...logForm, hours: Number(logForm.hours) };
      if (editingId) {
        await apiRequest(`/api/worklogs/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        showMessage("Work log updated successfully.");
      } else {
        await apiRequest("/api/worklogs", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showMessage("Work log created successfully.");
      }
      setLogForm(emptyLog);
      setEditingId(null);
      setView("dashboard");
      await loadLogs();
    } catch (err) {
      showError(err.message);
    }
  }

  function startCreateLog() {
    setEditingId(null);
    setLogForm(emptyLog);
    setView("log-form");
    setMessage("");
    setError("");
  }

  function startEditLog(log) {
    setEditingId(log.id);
    setLogForm({
      date: log.date,
      task: log.task,
      hours: String(log.hours),
      status: log.status,
      project: log.project,
      comments: log.comments || "",
    });
    setView("log-form");
    setMessage("");
    setError("");
  }

  async function deleteLog(logId) {
    if (!window.confirm("Are you sure you want to delete this work log?")) {
      return;
    }

    try {
      await apiRequest(`/api/worklogs/${logId}`, { method: "DELETE" });
      showMessage("Work log deleted successfully.");
      await loadLogs();
    } catch (err) {
      showError(err.message);
    }
  }

  return (
    <div>
      <header className="topbar">
        <div>
          <h1>WorkTrack</h1>
          <h2>Employee Work Log</h2>
          <p></p>
        </div>
        {user && (
          <button className="secondary" onClick={logout}>
            Logout
          </button>
        )}
      </header>

      <main className="container">
        {message && <div className="alert success">{message}</div>}
        {error && <div className="alert error">{error}</div>}

        {!user && view === "login" && (
          <section className="card narrow">
            <h2>Login</h2>
            <form onSubmit={login}>
              <label>Email</label>
              <input name="email" type="email" value={form.email} onChange={updateForm} required />
              <label>Password</label>
              <input name="password" type="password" value={form.password} onChange={updateForm} required />
              <button type="submit">Login</button>
            </form>
            <p className="muted">Admin: admin@example.com / admin123</p>
            <button className="link-button" onClick={() => setView("register")}>
              Create a new account
            </button>
          </section>
        )}

        {!user && view === "register" && (
          <section className="card narrow">
            <h2>Register</h2>
            <form onSubmit={register}>
              <label>Full name</label>
              <input name="full_name" value={form.full_name} onChange={updateForm} required />
              <label>Email</label>
              <input name="email" type="email" value={form.email} onChange={updateForm} required />
              <label>Password</label>
              <input name="password" type="password" value={form.password} onChange={updateForm} minLength="6" required />
              <button type="submit">Register</button>
            </form>
            <button className="link-button" onClick={() => setView("login")}>
              Back to login
            </button>
          </section>
        )}

        {user && view === "dashboard" && (
          <section className="card">
            <div className="dashboard-header">
              <div>
                <h2>Dashboard</h2>
                <p>
                  Logged in as <strong>{user.full_name}</strong> ({user.role})
                </p>
              </div>
              <button onClick={startCreateLog}>Add Work Log</button>
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Employee</th>
                    <th>Task</th>
                    <th>Hours</th>
                    <th>Status</th>
                    <th>Project</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log) => (
                    <tr key={log.id}>
                      <td>{log.date}</td>
                      <td>{log.user_full_name}</td>
                      <td>{log.task}</td>
                      <td>{log.hours}</td>
                      <td><span className="status">{log.status}</span></td>
                      <td>{log.project}</td>
                      <td className="actions">
                        <button className="small" onClick={() => startEditLog(log)}>Edit</button>
                        {user.role === "admin" && (
                          <button className="small danger" onClick={() => deleteLog(log.id)}>Delete</button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {user && view === "log-form" && (
          <section className="card narrow">
            <h2>{editingId ? "Edit Work Log" : "Create Work Log"}</h2>
            <form onSubmit={submitLog}>
              <label>Date</label>
              <input name="date" type="date" value={logForm.date} onChange={updateLogForm} required />
              <label>Task</label>
              <input name="task" value={logForm.task} onChange={updateLogForm} required />
              <label>Hours</label>
              <input name="hours" type="number" step="0.1" min="0.1" value={logForm.hours} onChange={updateLogForm} required />
              <label>Status</label>
              <select name="status" value={logForm.status} onChange={updateLogForm} required>
                <option>Pending</option>
                <option>In Progress</option>
                <option>Completed</option>
              </select>
              <label>Project</label>
              <input name="project" value={logForm.project} onChange={updateLogForm} required />
              <label>Comments</label>
              <textarea name="comments" value={logForm.comments} onChange={updateLogForm} />
              <button type="submit">{editingId ? "Save Changes" : "Create Log"}</button>
              <button type="button" className="secondary" onClick={() => setView("dashboard")}>Cancel</button>
            </form>
          </section>
        )}
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
