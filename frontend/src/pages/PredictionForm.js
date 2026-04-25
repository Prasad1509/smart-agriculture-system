import { useState } from "react";
import { predictCrop } from "../services/api";

function PredictionForm() {
  const [form, setForm] = useState({
    temperature: "",
    humidity: "",
    rainfall: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await predictCrop(form);
    alert("Prediction: " + res.data.prediction);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Crop Prediction</h2>

      <input placeholder="Temperature"
        onChange={(e)=>setForm({...form, temperature:e.target.value})} /><br/>

      <input placeholder="Humidity"
        onChange={(e)=>setForm({...form, humidity:e.target.value})} /><br/>

      <input placeholder="Rainfall"
        onChange={(e)=>setForm({...form, rainfall:e.target.value})} /><br/>

      <button type="submit">Predict</button>
    </form>
  );
}
export default PredictionForm;