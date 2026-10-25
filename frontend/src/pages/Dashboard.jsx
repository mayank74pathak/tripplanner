import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { generateItinerary, getItinerary } from "../services/api";

function formatDate(dateString) {
  if (!dateString) return "Date not set";

  const date = new Date(`${dateString}T00:00:00`);

  if (Number.isNaN(date.getTime())) return dateString;

  return date.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function formatBudget(budget) {
  const amount = Number(budget);

  if (!Number.isFinite(amount)) return "—";

  return `₹${amount.toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function Dashboard() {
  const navigate = useNavigate();

  const [trips, setTrips] = useState([]);
  const [itinerary, setItinerary] = useState("");
  const [selectedTripId, setSelectedTripId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tripLoading, setTripLoading] = useState(true);

  async function fetchTrips() {
    setTripLoading(true);
    setError("");

    try {
      const response = await api.get("/trips/");
      setTrips(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load your trips.");
    } finally {
      setTripLoading(false);
    }
  }

  useEffect(() => {
    fetchTrips();
  }, []);

  function logout() {
    localStorage.removeItem("access_token");
    navigate("/login");
  }

  async function deleteTrip(id) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this trip?",
    );

    if (!confirmed) return;

    try {
      await api.delete(`/trips/${id}`);

      setTrips((previousTrips) =>
        previousTrips.filter((trip) => trip.id !== id),
      );

      if (selectedTripId === id) {
        setSelectedTripId(null);
        setItinerary("");
      }

      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete this trip.");
    }
  }

  async function handleGenerateItinerary(tripId) {
    setSelectedTripId(tripId);
    setLoading(true);
    setError("");
    setItinerary("");

    try {
      const result = await generateItinerary(tripId);
      setItinerary(result.itinerary);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to generate the itinerary. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleViewItinerary(tripId) {
    setSelectedTripId(tripId);
    setLoading(true);
    setError("");
    setItinerary("");

    try {
      const result = await getItinerary(tripId);
      setItinerary(result.itinerary);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to load the saved itinerary.",
      );
    } finally {
      setLoading(false);
    }
  }

  const selectedTrip = trips.find((trip) => trip.id === selectedTripId);

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <Link to="/" className="brand" aria-label="Trip Planner home">
          <span className="brand-mark" aria-hidden="true">
            ✈
          </span>

          <span>
            <span className="brand-name">Trip Planner</span>
            <span className="brand-caption" style={{ display: "block" }}>
              Your next adventure starts here
            </span>
          </span>
        </Link>

        <div className="nav-actions">
          <Link to="/trips/create" className="btn btn-primary">
            <span aria-hidden="true">＋</span>
            Create Trip
          </Link>

          <button type="button" className="btn btn-secondary" onClick={logout}>
            Logout
          </button>
        </div>
      </nav>

      <main className="dashboard-main">
        <section className="dashboard-hero">
          <div>
            <p className="eyebrow">YOUR TRAVEL SPACE</p>
            <h1>Every great journey starts with a plan.</h1>
            <p>
              Organize your trips, manage your budget, and let AI help you plan
              memorable adventures.
            </p>
          </div>

          <div className="hero-illustration" aria-hidden="true">
            🌍
          </div>
        </section>

        {error && (
          <div className="error" role="alert" style={{ marginBottom: 24 }}>
            {error}
          </div>
        )}

        <section aria-labelledby="trips-heading">
          <div className="section-heading">
            <div>
              <h2 id="trips-heading">
                My Trips
                {!tripLoading && (
                  <span className="trip-count">{trips.length}</span>
                )}
              </h2>
              <p>All your upcoming adventures, in one place.</p>
            </div>

            {!tripLoading && trips.length > 0 && (
              <Link to="/trips/create" className="btn btn-secondary">
                + Add a trip
              </Link>
            )}
          </div>

          {tripLoading ? (
            <div className="state-card" role="status">
              <span className="spinner" aria-hidden="true" />
              <h3 style={{ marginTop: 18 }}>Loading your trips</h3>
              <p>Getting your travel plans ready...</p>
            </div>
          ) : trips.length === 0 ? (
            <div className="state-card">
              <div className="state-icon" aria-hidden="true">
                🧳
              </div>
              <h3>Your next adventure awaits</h3>
              <p>
                You haven't created a trip yet. Start planning somewhere you'd
                love to explore.
              </p>
              <Link to="/trips/create" className="btn btn-primary">
                + Create your first trip
              </Link>
            </div>
          ) : (
            <div className="trip-grid">
              {trips.map((trip) => (
                <article className="trip-card" key={trip.id}>
                  <div className="trip-card-top">
                    <div className="destination-icon" aria-hidden="true">
                      📍
                    </div>

                    <span className="trip-label">TRAVEL PLAN</span>
                  </div>

                  <h3>{trip.destination}</h3>

                  <p className="trip-dates">
                    <span aria-hidden="true">📅</span>
                    {formatDate(trip.start_date)}
                    <span aria-hidden="true">→</span>
                    {formatDate(trip.end_date)}
                  </p>

                  <div className="trip-details">
                    <div>
                      <span className="detail-label">Travelers</span>
                      <span className="detail-value">👥 {trip.travelers}</span>
                    </div>

                    <div>
                      <span className="detail-label">Total budget</span>
                      <span className="detail-value">
                        {formatBudget(trip.budget)}
                      </span>
                    </div>
                  </div>

                  <div className="trip-actions">
                    <Link
                      to={`/trips/${trip.id}/edit`}
                      className="btn btn-secondary"
                    >
                      ✎ Edit
                    </Link>

                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={() => handleGenerateItinerary(trip.id)}
                      disabled={loading}
                    >
                      {loading && selectedTripId === trip.id
                        ? "Generating..."
                        : "✦ Generate AI"}
                    </button>

                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => handleViewItinerary(trip.id)}
                      disabled={loading}
                    >
                      View itinerary
                    </button>

                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={() => deleteTrip(trip.id)}
                      disabled={loading}
                    >
                      Delete trip
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {loading && (
          <div className="itinerary-loading" role="status">
            <span className="spinner" aria-hidden="true" />

            <div>
              <strong>
                Planning {selectedTrip?.destination || "your trip"}...
              </strong>
              <p>
                Your itinerary is being processed. This may take a little time.
              </p>
            </div>
          </div>
        )}

        {itinerary && (
          <section
            className="itinerary-result"
            aria-labelledby="itinerary-heading"
          >
            <div className="itinerary-header">
              <div>
                <p className="eyebrow" style={{ marginBottom: 6 }}>
                  YOUR PERSONALIZED PLAN
                </p>
                <h2 id="itinerary-heading">
                  {selectedTrip?.destination
                    ? `${selectedTrip.destination} itinerary`
                    : "Your AI itinerary"}
                </h2>
                <p>A travel plan tailored to your trip.</p>
              </div>

              <span className="ai-badge">✦ AI GENERATED</span>
            </div>

            <div className="itinerary-content">
              <pre>{itinerary}</pre>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
