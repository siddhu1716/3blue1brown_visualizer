from typing import Dict, Any, List
import numpy as np
from manim import Scene, Axes, BarChart, VGroup, Create, Write, MathTex, BLUE, YELLOW

SCENE_KEY = "histogram_sampling"
PARAM_SCHEMA: Dict[str, Any] = {
    "data": "List[float] (optional)",
    "mean": "float (default 0.0 if data not provided)",
    "std": "float (default 1.0 if data not provided)",
    "n": "int number of samples when generating (default 500)",
    "bins": "int number of bins (default 20)",
}

class HistogramSamplingScene(Scene):
    def __init__(self, data: List[float] | None = None, mean: float = 0.0, std: float = 1.0, n: int = 500, bins: int = 20, **kwargs):
        super().__init__(**kwargs)
        self.data = np.array(data, dtype=float) if data is not None else None
        self.mean = float(mean)
        self.std = max(float(std), 1e-6)
        self.n = int(n)
        self.bins = int(bins)

    def construct(self):
        if self.data is None:
            self.data = np.random.normal(self.mean, self.std, size=self.n)

        counts, edges = np.histogram(self.data, bins=self.bins)
        values = counts.astype(float) / counts.max() if counts.max() > 0 else counts.astype(float)

        chart = BarChart(values=values.tolist(), y_range=[0, 1, 0.2], bar_names=[f"{edges[i]:.1f}\n{edges[i+1]:.1f}" for i in range(len(edges)-1)], bar_width=0.5)
        title = MathTex("\\text{Histogram}").to_edge(UP)
        self.play(Write(title))
        self.play(Create(chart))
        self.wait(1)

SCENE_CLASS = HistogramSamplingScene
