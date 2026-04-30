import React, { useState } from "react";
import "./App.css";
import Login from "./pages/Login";  // ✅ correct path

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("user_id") ? true : false
  );

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard />
      ) : (
        <Login onLogin={() => setIsLoggedIn(true)} />
      )}
    </div>
  );
}

// =====================================================
// 🔹 DASHBOARD COMPONENT
// =====================================================
function Dashboard() {
  const [temperature, setTemperature] = useState("");
  const [humidity, setHumidity] = useState("");
  const [rainfall, setRainfall] = useState("");
  const [output, setOutput] = useState("");
  const [historyData, setHistoryData] = useState([]);
  const [loading, setLoading] = useState(false);

  const user_id = localStorage.getItem("user_id");

  const predict = async () => {
    if (!temperature || !humidity || !rainfall) {
      setOutput("⚠️ Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const res = await fetch("http://127.0.0.1:5000/predict-db", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user_id,
          temperature: Number(temperature),
          humidity: Number(humidity),
          rainfall: Number(rainfall),
        }),
      });

      const data = await res.json();

      if (data.predicted_crop) {
        setOutput("🌾 Predicted Crop: " + data.predicted_crop);
      } else {
        setOutput("❌ Error: " + (data.error || "Something went wrong"));
      }
    } catch (error) {
      setOutput("❌ Server error");
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/predictions/${user_id}`
      );
      const data = await res.json();

      if (Array.isArray(data)) {
        setHistoryData(data);
      }
    } catch (error) {
      setOutput("❌ Error loading history");
    }
  };

  const logout = () => {
    localStorage.removeItem("user_id");
    window.location.reload();
  };

  return (
    <div className="App">
      <h1>🌾 Smart Agriculture System</h1>

      <button onClick={logout}>Logout</button>

      <div className="card">
        <h2>Crop Prediction</h2>

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

        <button onClick={predict}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        <button onClick={loadHistory}>Show History</button>

        <h3>{output}</h3>
      </div>

      <div className="card">
        <h2>Prediction History</h2>

        {historyData.length === 0 ? (
          <p>No data available</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Temp</th>
                <th>Humidity</th>
                <th>Rainfall</th>
                <th>Crop</th>
              </tr>
            </thead>
            <tbody>
              {historyData.map((item, index) => (
                <tr key={index}>
                  <td>{item.temperature}</td>
                  <td>{item.humidity}</td>
                  <td>{item.rainfall}</td>
                  <td>{item.predicted_crop}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;