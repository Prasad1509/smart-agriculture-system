import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div>
      <h2>Dashboard</h2>
      <Link to="/predict">Go to Prediction</Link>
    </div>
  );
}
export default Dashboard;