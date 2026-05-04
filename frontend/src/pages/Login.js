import React, { useState } from "react";
import "./Login.css";

function Login({ onLogin }) {   // ✅ receive prop
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      setMessage("⚠️ Please fill all fields");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await res.json();

      if (res.status === 200) {
        setMessage("✅ Login Successful");

        // ✅ Save user_id
        localStorage.setItem("user_id", data.user_id);

        // ✅ VERY IMPORTANT (tell App login done)
        onLogin();   // 🔥 THIS WAS MISSING
      } else {
        setMessage("❌ " + data.message);
      }

    } catch (error) {
      setMessage("❌ Server Error");
    }
  };

  return (
    <div className="login-container">
      <h2>🔐 Login</h2>

      <input
        type="email"
        placeholder="Enter Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>

      <p>{message}</p>
    </div>
  );
}

export default Login;