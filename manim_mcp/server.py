import sys
import os
import json
import argparse
import tempfile
from typing import Dict, Any, List

from manim import config, tempconfig
from manim import Scene, VGroup, Axes, Dot, Line, MathTex, Square, FadeIn, FadeOut, Create, Write, Transform
from manim import BLUE, YELLOW, WHITE
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

RENDERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'renders'))
os.makedirs(RENDERS_DIR, exist_ok=True)

# -----------------
# Scene Definitions
# -----------------
class FourierSquareWave(Scene):
    def __init__(self, terms: List[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.terms = terms or [1, 3, 5, 7, 9]

    def construct(self):
        axes = Axes(x_range=[0, 2 * np.pi, np.pi/2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("f(x)"))
        self.play(Create(axes), Write(labels))

        x = np.linspace(0, 2 * np.pi, 1000)

        # Square wave target
        def square_wave(x):
            return np.sign(np.sin(x))

        target_graph = axes.plot(square_wave, x_range=[0, 2*np.pi], color=YELLOW)
        self.play(Create(target_graph))

        # Build Fourier approximation progressively
        partial_sum = np.zeros_like(x)
        graphs = VGroup()
        for k in self.terms:
            partial_sum += (4 / (np.pi * k)) * np.sin(k * x)
            approx_func = lambda t, ps=partial_sum.copy(): np.interp(t, x, ps)
            graph = axes.plot(approx_func, x_range=[0, 2*np.pi], color=BLUE)
            graphs.add(graph)
            if len(graphs) == 1:
                self.play(Create(graph))
            else:
                self.play(Transform(graphs[-2], graph))
        
        self.wait(1)

# ---------------
# Render Helpers
# ---------------
SCENE_REGISTRY = {
    "fourier_series": FourierSquareWave,
}

def render_request(req: Dict[str, Any]) -> str:
    vis_type = req.get("type") or req.get("visualization_type")
    params = req.get("parameters", {})

    if vis_type not in SCENE_REGISTRY:
        # Fallback: create a minimal scene
        class Placeholder(Scene):
            def construct(self):
                self.play(Write(MathTex("Unsupported~visualization")))
                self.wait(1)
        scene_cls = Placeholder
        scene_name = "Placeholder"
    else:
        scene_cls = SCENE_REGISTRY[vis_type]
        scene_name = scene_cls.__name__

    # Output path
    out_name = f"{vis_type or 'visualization'}.mp4"
    out_path = os.path.join(RENDERS_DIR, out_name)

    # Render with manim tempconfig to control output dir
    with tempconfig({
        "media_dir": RENDERS_DIR,
        "video_dir": RENDERS_DIR,
        "images_dir": os.path.join(RENDERS_DIR, "images"),
        "log_to_file": False,
        "format": "mp4",
        "write_to_movie": True,
        "save_last_frame": False,
        "pixel_width": 1280,
        "pixel_height": 720,
        "frame_rate": 30,
    }):
        scene = scene_cls(**params)
        scene.render()  # Manim determines file path

    # Find the latest mp4 produced
    produced_files = [f for f in os.listdir(RENDERS_DIR) if f.endswith('.mp4')]
    if not produced_files:
        raise RuntimeError("No video produced")
    produced_files.sort(key=lambda f: os.path.getmtime(os.path.join(RENDERS_DIR, f)), reverse=True)
    latest = os.path.join(RENDERS_DIR, produced_files[0])
    return latest

# ---------------
# CLI Entrypoint
# ---------------

def main():
    parser = argparse.ArgumentParser(description="Manim MCP Server")
    parser.add_argument('--http', action='store_true', help='Run as HTTP server (FastAPI)')
    parser.add_argument('--host', default='0.0.0.0', help='HTTP host')
    parser.add_argument('--port', type=int, default=9000, help='HTTP port')
    parser.add_argument('request_file', nargs='?', help='Path to JSON request file produced by backend (CLI mode)')
    args = parser.parse_args()

    if args.http:
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port)
        return

    if not args.request_file:
        parser.error('request_file is required in CLI mode')

    with open(args.request_file, 'r') as f:
        req = json.load(f)

    out_path = render_request(req)
    # Print absolute path for caller
    print(os.path.abspath(out_path))

# ---------------
# HTTP (FastAPI)
# ---------------

class RenderRequest(BaseModel):
    visualization_type: str | None = None
    type: str | None = None
    parameters: dict = {}

class RenderResponse(BaseModel):
    video_path: str

def create_app() -> FastAPI:
    app = FastAPI(title="Manim MCP Server", version="1.0.0")

    @app.get('/health')
    async def health():
        return {"status": "ok"}

    @app.post('/render', response_model=RenderResponse)
    async def render(req: RenderRequest):
        data = {
            "type": req.type or req.visualization_type,
            "parameters": req.parameters or {},
        }
        out_path = render_request(data)
        return RenderResponse(video_path=os.path.abspath(out_path))

    return app

if __name__ == '__main__':
    main()
