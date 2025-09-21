# 3blue1brown_visualizer
Local-first web app: type a natural language prompt → an LLM refines it into a structured request → the Manim MCP server renders a visualization → the result is displayed in the browser.

## Repo Structure

```
.
├── frontend/              # Next.js (App Router) + Tailwind + shadcn-style UI
├── backend/               # FastAPI orchestration + LLM refinement + MCP client
├── manim_mcp/             # Manim MCP server (CLI and HTTP) + scenes
├── renders/               # Generated animations (shared volume)
├── docker-compose.yml     # One-command setup
└── README.md
```

## Core Flow

- Input a prompt in `frontend` UI.
- `backend` refines it with LLM (OpenAI or local Ollama). Falls back to mock if none configured.
- `backend` calls `manim_mcp` (HTTP or CLI fallback) to render.
- `backend` serves the resulting file under `/renders/...`.
- `frontend` displays the video using a simple player.

## Quick Start (Docker Compose)

Requirements: Docker Desktop or Docker Engine

1) Optionally set your LLM provider via env vars (create a `.env` next to `docker-compose.yml`):

```
# Use OpenAI (optional)
OPENAI_API_KEY=sk-your-key

# Or use local Ollama (optional)
USE_OLLAMA=true
OLLAMA_URL=http://host.docker.internal:11434
```

2) Launch all services:

```
docker compose up --build
```

3) Open the app:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/health
- Manim MCP: http://localhost:9000/health

4) Try a prompt like:

- "Show me how a Fourier series builds a square wave"

If LLMs aren’t configured, the backend uses a smart mock that routes this to a Fourier demo.

## Local Development (without Docker)

Prereqs: Node 18+, Python 3.11+, ffmpeg, Manim dependencies

1) Start Manim MCP (HTTP mode):

```
# In a new terminal
python -m venv .venv-manim
source .venv-manim/bin/activate
pip install -r manim_mcp/requirements.txt
python manim_mcp/server.py --http --host 0.0.0.0 --port 9000
```

2) Start backend:

```
# In a new terminal
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
# Optional: export OPENAI_API_KEY or USE_OLLAMA/OLLAMA_URL
export MANIM_MCP_URL=http://localhost:9000
python backend/main.py
```

- Backend will serve renders under `http://localhost:8000/renders/...` (files stored in `renders/`).

3) Start frontend:

```
# In a new terminal
cd frontend
npm install
# To develop:
npm run dev
# To build & serve:
# NEXT_PUBLIC_BACKEND_URL can be used to override backend URL if needed
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 npm run build
npm start
```

Open http://localhost:3000 and generate a visualization.

## How It Works

- `backend/llm.py`
  - Chooses provider based on env:
    - `OPENAI_API_KEY` for OpenAI.
    - `USE_OLLAMA=true` and `OLLAMA_URL` for Ollama.
  - If neither is set, uses a deterministic mock mapper (Fourier, linear transform, etc.).
  - Produces a structured JSON request like:

```
{
  "visualization_type": "fourier_series",
  "parameters": { "terms": [1,3,5,7,9], "target_function": "square_wave" },
  "description": "Fourier series approximation of a square wave using odd harmonics"
}
```

- `backend/mcp_client.py`
  - Calls Manim MCP via HTTP if `MANIM_MCP_URL` is set.
  - Otherwise falls back to invoking `manim_mcp/server.py` in CLI mode.
  - Ensures results end up in shared `renders/` directory.

- `manim_mcp/server.py`
  - CLI mode: `python server.py path/to/request.json` prints the generated absolute video path.
  - HTTP mode (FastAPI): `POST /render` with `{ type, parameters }` returns `{ video_path }`.
  - Includes a demo scene: Fourier series approximation of a square wave.

## Adding New MCP Endpoints / Scenes

1) Create a new Scene in `manim_mcp/server.py` or a module under `manim_mcp/scenes/` and import it.
2) Register it in `SCENE_REGISTRY`, e.g.:

```python
SCENE_REGISTRY = {
  "fourier_series": FourierSquareWave,
  "linear_transform": LinearTransformScene,
}
```

3) Extend `backend/llm.py` to emit a new `visualization_type` and expected `parameters`.

## Troubleshooting

- No video renders / empty file:
  - Ensure `ffmpeg` is installed in your environment. Docker images include it.
  - Check `renders/` permissions and that the volume is mounted in Docker.
- Frontend can’t load video:
  - Confirm `NEXT_PUBLIC_BACKEND_URL` is correct (defaults to backend service in Docker, localhost in dev).
  - Videos are proxied from `/renders/...` via Next.js rewrites to backend.
- Manim errors:
  - Watch `docker compose logs manim_mcp` or your terminal where MCP runs.
- LLM errors:
  - If no provider is set, the backend mock still returns a valid structured request for demos.

## Stretch Goals

- More MCP endpoints for common math visualizations (linear transforms, eigen demos, function plots, Taylor series, etc.).
- Interactive controls (sliders for frequency, matrix entries).
- Tutor Mode: have the LLM return explanatory text alongside the visualization.

## License

MIT
