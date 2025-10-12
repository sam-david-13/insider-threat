// ============= GLOBAL VARIABLES =============
const API_BASE = "http://127.0.0.1:5000/api";

// ============= NAVIGATION LOGIC =============
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".nav-btn");
  const views = document.querySelectorAll(".view");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const view = btn.getAttribute("data-view");

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      views.forEach(v => v.classList.add("hidden"));
      document.getElementById(view).classList.remove("hidden");

      // Load content based on selected view
      if (view === "users") loadUsers();
      if (view === "activities") loadActivityLogs();
      if (view === "anomalies") loadAnomalies();
      if (view === "files") loadFileAccessSim();
    });
  });

  // Load Overview by default
  document.querySelector(".nav-btn[data-view='overview']").click();
});

// ============= LOAD USERS =============
async function loadUsers() {
  const container = document.querySelector(".user-grid");
  container.innerHTML = "<p>Loading users...</p>";

  try {
    const res = await fetch(`${API_BASE}/users`);
    const users = await res.json();

    container.innerHTML = users.map(u => `
      <div class="user-card" onclick="analyzeUser('${u.id}')">
        <img src="https://cdn-icons-png.flaticon.com/512/2922/2922510.png" alt="User">
        <h4>${u.name}</h4>
        <p>${u.role} - ${u.department}<br>Status: ${u.status}</p>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<p style='color:red;'>Error loading users.</p>`;
    console.error(err);
  }
}

// ============= LOAD ACTIVITY LOGS =============
async function loadActivityLogs() {
  const logContainer = document.getElementById("activity-log");
  logContainer.innerHTML = "<p>Loading activity logs...</p>";

  try {
    const res = await fetch(`${API_BASE}/activities`);
    const logs = await res.json();

    if (!logs.length) {
      logContainer.innerHTML = "<p>No activity logs found.</p>";
      return;
    }

    logContainer.innerHTML = logs.map(l => `
      <div class="log-entry">
        <strong>${l.user_id}</strong> — ${l.activity}<br>
        <small>${new Date(l.timestamp).toLocaleString()}</small>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
    logContainer.innerHTML = `<p style='color:red;'>Failed to load logs.</p>`;
  }
}

// ============= LOAD ANOMALIES =============
async function loadAnomalies() {
  const container = document.getElementById("anomalies");
  container.innerHTML = "<h1>⚠️ Anomaly Detection</h1><p>Loading anomalies...</p>";

  try {
    const res = await fetch(`${API_BASE}/anomalies`);
    const anomalies = await res.json();

    if (!anomalies.length) {
      container.innerHTML += "<p>No anomalies found.</p>";
      return;
    }

    container.innerHTML = `
      <h1>⚠️ Anomaly Detection</h1>
      <div class="anomaly-grid">
        ${anomalies.map(a => `
          <div class="anomaly-card" style="border-left:5px solid ${a.threat_score > 70 ? 'red' : a.threat_score > 40 ? 'orange' : 'green'}">
            <h3>${a.user_id}</h3>
            <p>${a.reason}</p>
            <strong>Threat Score: ${a.threat_score}%</strong>
            <small>${new Date(a.timestamp).toLocaleString()}</small>
          </div>
        `).join("")}
      </div>
    `;
  } catch (err) {
    console.error(err);
    container.innerHTML = "<p style='color:red;'>Failed to load anomalies.</p>";
  }
}

// ============= SIMULATE CONFIDENTIAL FILE ACCESS =============
async function loadFileAccessSim() {
  const container = document.getElementById("file-access-container");
  container.innerHTML = `
    <div>
      <input type="text" id="fileUser" placeholder="Enter User ID (e.g., EMP001)">
      <button onclick="simulateFileAccess()">Simulate Access</button>
    </div>
    <div id="file-access-result" style="margin-top:1rem;"></div>
  `;
}

async function simulateFileAccess() {
  const userId = document.getElementById("fileUser").value.trim();
  const resultBox = document.getElementById("file-access-result");

  if (!userId) {
    resultBox.innerHTML = "<p style='color:red;'>Please enter a valid user ID.</p>";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/confidential_files`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId })
    });
    const data = await res.json();

    // Create paragraph element
    const p = document.createElement("p");
    p.textContent = data.message;

    // Add class based on access status
    if (data.access_status === "SUCCESS") {
      p.classList.add("success");
    } else if (data.access_status === "DENIED") {
      p.classList.add("denied");
    }

    // Clear previous and append new
    resultBox.innerHTML = "";
    resultBox.appendChild(p);

  } catch (err) {
    console.error(err);
    resultBox.innerHTML = "<p style='color:red;'>Failed to simulate access.</p>";
  }
}

// ============= ANALYZE USER (THREAT SCORE) =============
async function analyzeUser(userId) {
  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId })
    });
    const data = await res.json();

    alert(`User ${data.user_id} has a Threat Score of ${data.threat_score}%`);
    loadAnomalies(); // Refresh anomalies
  } catch (err) {
    console.error(err);
  }
}
const resultBox = document.getElementById("file-access-result");

// Assuming `data.message` comes from Python API
const p = document.createElement("p");
p.textContent = data.message;

// Add class based on text
if (data.message.includes("DENIED")) {
    p.classList.add("denied");
} else if (data.message.includes("SUCCESS")) {
    p.classList.add("success");
}

resultBox.innerHTML = ""; // clear previous
resultBox.appendChild(p);
