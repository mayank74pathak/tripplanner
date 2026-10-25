import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api from "../services/api";

function EditTrip() {
  const { id } = useParams();

  const navigate = useNavigate();

  const [form, setForm] = useState(null);

  useEffect(() => {
    async function fetchTrip() {
      try {
        const response = await api.get(`/trips/${id}`);

        const trip = response.data;

        setForm({
          destination: trip.destination,
          start_date: trip.start_date,
          end_date: trip.end_date,
          travelers: trip.travelers,
          budget: trip.budget,
        });
      } catch (error) {
        alert("Failed to load trip");

        navigate("/dashboard");
      }
    }

    fetchTrip();
  }, [id, navigate]);

  if (!form) {
    return <p>Loading...</p>;
  }

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await api.put(`/trips/${id}`, {
        destination: form.destination,
        start_date: form.start_date,
        end_date: form.end_date,
        travelers: Number(form.travelers),
        budget: Number(form.budget),
      });

      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.detail || "Failed to update trip");
    }
  }

  return (
    <div className="form-page">
      <div className="form-card">
        <h1>Edit Trip</h1>

        <form onSubmit={handleSubmit}>
          <label>Destination</label>

          <input
            name="destination"
            value={form.destination}
            onChange={handleChange}
          />

          <label>Start Date</label>

          <input
            type="date"
            name="start_date"
            value={form.start_date}
            onChange={handleChange}
          />

          <label>End Date</label>

          <input
            type="date"
            name="end_date"
            value={form.end_date}
            onChange={handleChange}
          />

          <label>Travelers</label>

          <input
            type="number"
            name="travelers"
            min="1"
            value={form.travelers}
            onChange={handleChange}
          />

          <label>Budget</label>

          <input
            type="number"
            name="budget"
            value={form.budget}
            onChange={handleChange}
          />

          <button type="submit">Update Trip</button>
        </form>
      </div>
    </div>
  );
}

export default EditTrip;
