import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

function CreateTrip() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    destination: "",
    start_date: "",
    end_date: "",
    travelers: 1,
    budget: "",
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await api.post("/trips/", {
        destination: form.destination,

        start_date: form.start_date,

        end_date: form.end_date,

        travelers: Number(form.travelers),

        budget: Number(form.budget),
      });

      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.detail || "Failed to create trip");
    }
  }

  return (
    <div className="form-page">
      <div className="form-card">
        <h1>Create Trip</h1>

        <form onSubmit={handleSubmit}>
          <label>Destination</label>

          <input
            name="destination"
            placeholder="e.g. Goa"
            value={form.destination}
            onChange={handleChange}
            required
          />

          <label>Start Date</label>

          <input
            type="date"
            name="start_date"
            value={form.start_date}
            onChange={handleChange}
            required
          />

          <label>End Date</label>

          <input
            type="date"
            name="end_date"
            value={form.end_date}
            onChange={handleChange}
            required
          />

          <label>Number of Travelers</label>

          <input
            type="number"
            name="travelers"
            min="1"
            value={form.travelers}
            onChange={handleChange}
            required
          />

          <label>Budget</label>

          <input
            type="number"
            name="budget"
            placeholder="30000"
            value={form.budget}
            onChange={handleChange}
            required
          />

          <button type="submit">Create Trip</button>
        </form>
      </div>
    </div>
  );
}

export default CreateTrip;
