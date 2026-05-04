import React, { useState } from "react";
import "./App.css";
import Login from "./pages/Login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 🔥 force login

  return (
    <div>
      {!isLoggedIn ? (
        <Login onLogin={() => setIsLoggedIn(true)} />
      ) : (
        <h2>✅ Dashboard</h2>
      )}
    </div>
  );
}

// ================= DASHBOARD =================
function Dashboard() {
  const [temperature, setTemperature] = useState("");
  const [humidity, setHumidity] = useState("");
  const [rainfall, setRainfall] = useState("");
  const [output, setOutput] = useState("");
  const [historyData, setHistoryData] = useState([]);

  const user_id = localStorage.getItem("user_id") || 1;

  const predict = async () => {
    const res = await fetch("http://127.0.0.1:5000/predict-db", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id,
        temperature,
        humidity,
        rainfall
      })
    });

    const data = await res.json();
    setOutput("🌾 " + data.predicted_crop);
  };

  const loadHistory = async () => {
    const res = await fetch(
      `http://127.0.0.1:5000/predictions/${user_id}`
    );
    const data = await res.json();
    setHistoryData(data);
  };

  return (
    <div>
      <h1>🌾 Smart Agriculture</h1>

      <input placeholder="Temp" onChange={(e) => setTemperature(e.target.value)} />
      <input placeholder="Humidity" onChange={(e) => setHumidity(e.target.value)} />
      <input placeholder="Rainfall" onChange={(e) => setRainfall(e.target.value)} />

      <button onClick={predict}>Predict</button>
      <button onClick={loadHistory}>History</button>

      <h3>{output}</h3>

      {historyData.map((item, i) => (
        <p key={i}>
          {item.temperature} | {item.humidity} | {item.rainfall} → {item.predicted_crop}
        </p>
      ))}
    </div>
  );
}

export default App;