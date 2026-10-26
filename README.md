#  AI Trip Planner

An AI-powered travel planning application that generates personalized, budget-aware travel itineraries based on a user's destination, travel duration, budget, and preferences.

The project combines **Generative AI, full-stack development, and Model Context Protocol (MCP)** to create a foundation for an intelligent travel assistant.

## 🚀 Features

- **AI-Powered Itinerary Generation** — Generate day-by-day travel plans using OpenAI.
- **Personalized Trip Planning** — Plan trips based on destination, duration, budget, and traveler requirements.
- **User Authentication** — JWT-based authentication and protected APIs.
- **Trip Management** — Create, view, update, and delete trips.
- **Budget-Aware Planning** — Generate itineraries with estimated travel expenses.
- **MCP Tool Integration** — MCP server for attraction discovery and trip cost estimation.
- **REST API** — FastAPI backend for frontend and AI workflow integration.
- **Persistent Storage** — PostgreSQL database for users and trip information.
- **Responsive Frontend** — React and Vite-based user interface.

> Note: Features such as live prices, weather forecasts, and real-time booking are not included unless separately integrated.

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| AI | OpenAI API, Generative AI |
| Tool Integration | Model Context Protocol (MCP), Python |
| Authentication | JWT |
| API Communication | REST, Axios |
| Version Control | Git, GitHub |

## 🏗️ Architecture

```text
                 ┌──────────────────────┐
                 │    React Frontend    │
                 │   React + Vite       │
                 └──────────┬───────────┘
                            │ REST API
                 ┌──────────▼───────────┐
                 │    FastAPI Backend   │
                 │ Authentication       │
                 │ Trip Management      │
                 │ AI Orchestration     │
                 └──────┬─────────┬─────┘
                        │         │
              ┌─────────▼──┐  ┌───▼────────────┐
              │ PostgreSQL │  │  OpenAI API    │
              │ Trip Data  │  │ Itinerary AI   │
              └────────────┘  └────────┬───────┘
                                       │
                              ┌────────▼────────┐
                              │    MCP Server   │
                              │ Attraction Tools│
                              │ Cost Estimation │
                              └─────────────────┘
```

*The MCP server participates in the AI workflow only when the backend is configured to discover and invoke its tools.*

## 📁 Project Structure

```text
trip-planner/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── services/
│   │   └── ...
│   ├── requirements.txt
│   └── .env
├── mcp-server/
│   ├── server.py
│   └── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

*The directory structure above is illustrative; adjust it to match the actual files in your repository.*

## ⚙️ Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version supported by your dependencies
- Node.js and npm
- PostgreSQL
- An OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/mayank74pathak/tripplanner.git
cd tripplanner
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=your_postgresql_connection_string
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini
SECRET_KEY=your_secure_random_secret
MCP_SERVER_URL=http://127.0.0.1:8001/mcp
FRONTEND_URL=http://localhost:5173
```

Replace the example values with your actual configuration. Ensure the database exists and the required schema or migrations have been applied.

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 3. Set Up the MCP Server

Open a separate terminal:

```bash
cd mcp-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

Confirm that the MCP server is running and that `MCP_SERVER_URL` matches the actual Streamable HTTP endpoint configured in `server.py`.

### 4. Set Up the Frontend

Open another terminal:

```bash
cd frontend
npm install
```

Configure the frontend API base URL according to the variable used by your Axios service:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Open the local URL printed by Vite, usually http://localhost:5173.

## 🔐 Security

- Never commit API keys, database passwords, JWT secrets, or `.env` files.
- Use environment variables for sensitive configuration.
- Keep authentication and authorization checks on the backend.
- Restrict CORS to trusted frontend origins in production.
- Use HTTPS and secure production secrets when deploying.

## 🌐 Deployment

The application can be deployed using separate services:

- **Frontend:** Vercel or Netlify
- **FastAPI backend:** Render or another Python hosting provider
- **Database:** Managed PostgreSQL
- **MCP server:** A separate service supporting persistent Streamable HTTP connections

Configure production environment variables and service URLs before deployment. Never expose the OpenAI API key in frontend code.

## 🗺️ Future Enhancements

- Interactive maps and optimized sightseeing routes
- Conversational itinerary editing
- Weather-aware recommendations
- Advanced budget optimization
- Retrieval-augmented generation (RAG) for travel knowledge
- Exportable PDF itineraries
- Automated API and AI workflow tests
- CI/CD and production monitoring

## 👨‍💻 Author

**Mayank Pathak**

GitHub: [@mayank74pathak](https://github.com/mayank74pathak)

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
