import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import PredictionForm from "./pages/PredictionForm";
import Result from "./pages/Result";

function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/predict" element={<PredictionForm />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;