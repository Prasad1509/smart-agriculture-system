import React, { useState } from "react";
import "./App.css";
import Login from "./pages/Login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div>
      {!isLoggedIn ? (
        <Login
          onLogin={() => {
            console.log("Login success trigger"); // ✅ DEBUG
            setIsLoggedIn(true);
          }}
        />
      ) : (
        <Dashboard />
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

  // 🔹 Predict
  const predict = async () => {
    console.log("Predict button clicked"); // ✅ DEBUG

    try {
      const res = await fetch("http://127.0.0.1:5000/predict-db", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id,
          temperature: Number(temperature),
          humidity: Number(humidity),
          rainfall: Number(rainfall)
        })
      });

      const data = await res.json();

      console.log("Prediction Response:", data); // ✅ DEBUG

      if (data.predicted_crop) {
        setOutput("🌾 " + data.predicted_crop);
      } else {
        setOutput("❌ Error");
      }

    } catch (error) {
      console.log(error);
      setOutput("❌ Server error");
    }
  };

  // 🔹 Load History
  const loadHistory = async () => {
    console.log("History button clicked"); // ✅ DEBUG

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/predictions/${user_id}`
      );

      const data = await res.json();

      console.log("History:", data); // ✅ DEBUG

      if (Array.isArray(data)) {
        setHistoryData(data);
      } else {
        setHistoryData([]);
      }

    } catch (error) {
      console.log(error);
      setOutput("❌ Error loading history");
    }
  };

  return (
    <div>
      <h1>🌾 Smart Agriculture</h1>

      <input
        placeholder="Temperature"
        value={temperature}
        onChange={(e) => setTemperature(e.target.value)}
      />

      <input
        placeholder="Humidity"
        value={humidity}
        onChange={(e) => setHumidity(e.target.value)}
      />

      <input
        placeholder="Rainfall"
        value={rainfall}
        onChange={(e) => setRainfall(e.target.value)}
      />

      <br /><br />

      <button onClick={predict}>Predict</button>
      <button onClick={loadHistory}>History</button>

      <h3>{output}</h3>

      <div>
        {historyData.map((item, i) => (
          <p key={i}>
            {item.temperature} | {item.humidity} | {item.rainfall} →{" "}
            {item.predicted_crop}
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;