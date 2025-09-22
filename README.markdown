# 3blue1brown Visualizer

A local-first web app that transforms natural language prompts into stunning mathematical visualizations using a combination of LLM refinement and Manim MCP rendering. Type a prompt, and watch as it’s refined into a structured request, rendered as a visualization, and displayed in your browser.

## Example Visualization

Below is an example of a generated visualization: a Fourier series approximation of a square wave.

![Fourier Square Wave Demo](renders/FourierSquareWave.gif)

## User Interface

Here’s a glimpse of the app’s intuitive UI, designed for seamless interaction:

![UI Screenshot](image.png)

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

1. **Input Prompt**: Enter a natural language prompt in the `frontend` UI (e.g., "Show me how a Fourier series builds a square wave").
2. **LLM Refinement**: The `backend` refines the prompt using an LLM (OpenAI or local Ollama) into a structured JSON request. A mock fallback is used if no LLM is configured.
3. **Visualization Rendering**: The `backend` sends the request to the `manim_mcp` server (via HTTP or CLI) to render the visualization.
4. **Result Storage**: The rendered video is saved in the `renders/` directory and served by the `backend` at `/renders/...`.
5. **Display and Explanation**: The `frontend` displays the video in a sleek player, and the `backend` provides an LLM-generated explanation to help users understand the visualization.

## Quick Start (Docker Compose)

### Requirements
- Docker Desktop or Docker Engine

### Steps
1. **Configure LLM (Optional)**  
   Create a `.env` file next to `docker-compose.yml` to set your LLM provider:
   ```
   # Use OpenAI (optional)
   OPENAI_API_KEY=sk-your-key

   # Or use local Ollama (optional)
   USE_OLLAMA=true
   OLLAMA_URL=http://host.docker.internal:11434
   ```

2. **Launch Services**  
   Run the following command to start all services:
   ```
   docker compose up --build
   ```

3. **Access the App**  
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://localhost:8000/health](http://localhost:8000/health)
   - Manim MCP: [http://localhost:9000/health](http://localhost:9000/health)

4. **Try a Prompt**  
   Enter a prompt like:
   - "Show me how a Fourier series builds a square wave"  
   If no LLM is configured, the backend uses a mock to map this to a Fourier demo, and an explanation is provided alongside the visualization.

## Local Development (Without Docker)

### Prerequisites
- Node.js 18+
- Python 3.11+
- `ffmpeg`
- Manim dependencies

### Steps
1. **Start Manim MCP (HTTP Mode)**  
   In a new terminal:
   ```
   python -m venv .venv-manim
   source .venv-manim/bin/activate
   pip install -r manim_mcp/requirements.txt
   python manim_mcp/server.py --http --host 0.0.0.0 --port 9000
   ```

2. **Start Backend**  
   In a new terminal:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   # Optional: export LLM env vars (OPENAI_API_KEY or USE_OLLAMA/OLLAMA_URL)
   export MANIM_MCP_URL=http://localhost:9000
   python backend/main.py
   ```
   The backend serves renders at `http://localhost:8000/renders/...` (stored in `renders/`).

3. **Start Frontend**  
   In a new terminal:
   ```
   cd frontend
   npm install
   # For development:
   npm run dev
   # For production build & serve:
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 npm run build
   npm start
   ```

4. **Access the App**  
   Open [http://localhost:3000](http://localhost:3000) and generate a visualization with an accompanying explanation.

## How It Works

- **`backend/llm.py`**  
  - Selects LLM provider based on environment variables:
    - `OPENAI_API_KEY` for OpenAI.
    - `USE_OLLAMA=true` and `OLLAMA_URL` for Ollama.
    - Falls back to a deterministic mock mapper if no LLM is configured.
  - Generates a structured JSON request, e.g.:
    ```
    {
      "visualization_type": "fourier_series",
      "parameters": { "terms": [1,3,5,7,9], "target_function": "square_wave" },
      "description": "Fourier series approximation of a square wave using odd harmonics",
      "explanation": "This visualization shows how a square wave can be approximated by summing sine waves with odd harmonics, as described by the Fourier series."
    }
    ```

- **`backend/mcp_client.py`**  
  - Communicates with `manim_mcp` via HTTP if `MANIM_MCP_URL` is set, or falls back to CLI mode.
  - Stores rendered videos in the shared `renders/` directory.

- **`manim_mcp/server.py`**  
  - **CLI Mode**: `python server.py path/to/request.json` outputs the absolute video path.
  - **HTTP Mode**: `POST /render` with `{ type, parameters }` returns `{ video_path }`.
  - Includes a demo scene: Fourier series approximation of a square wave.

## Adding New Visualizations

1. **Create a Scene**  
   Add a new Manim scene in `manim_mcp/server.py` or under `manim_mcp/scenes/`, and import it.

2. **Register the Scene**  
   Update `SCENE_REGISTRY` in `manim_mcp/server.py`:
   ```python
   SCENE_REGISTRY = {
     "fourier_series": FourierSquareWave,
     "linear_transform": LinearTransformScene,
     # Add new scene here
   }
   ```

3. **Extend LLM Mapping**  
   Update `backend/llm.py` to support the new `visualization_type` and its required `parameters`.

## Troubleshooting

- **No Video Renders / Empty File**  
  - Ensure `ffmpeg` is installed (included in Docker images).
  - Verify `renders/` directory permissions and Docker volume mounting.
- **Frontend Can’t Load Video**  
  - Check that `NEXT_PUBLIC_BACKEND_URL` is correct (defaults to backend service in Docker, localhost in dev).
  - Videos are proxied from `/renders/...` via Next.js rewrites.
- **Manim Errors**  
  - Check logs: `docker compose logs manim_mcp` or the terminal running MCP.
- **LLM Errors**  
  - If no LLM is configured, the mock ensures valid demo requests with explanations.

## Stretch Goals

- Add more visualizations (e.g., linear transformations, eigenvalue demos, function plots, Taylor series).
- Introduce interactive controls (e.g., sliders for frequencies or matrix entries).
- Enhance Tutor Mode with richer LLM-generated explanations alongside visualizations.

## License

Apache2.0
