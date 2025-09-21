from typing import Dict, Any
import numpy as np
from manim import Scene, Axes, MathTex, Create, Write, BLUE

SCENE_KEY = "normal_distribution"
PARAM_SCHEMA: Dict[str, Any] = {
    "mean": "float (default 0.0)",
    "std": "float > 0 (default 1.0)",
    "x_min": "float (default -4)",
    "x_max": "float (default 4)",
}

class NormalDistributionScene(Scene):
    def __init__(self, mean: float = 0.0, std: float = 1.0, x_min: float = -4.0, x_max: float = 4.0, **kwargs):
        super().__init__(**kwargs)
        self.mean = float(mean)
        self.std = max(float(std), 1e-3)
        self.x_min = float(x_min)
        self.x_max = float(x_max)

    def construct(self):
        axes = Axes(x_range=[self.x_min, self.x_max, (self.x_max - self.x_min)/4], y_range=[0, 0.5, 0.1], x_length=10, y_length=4)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("p(x)"))
        self.play(Create(axes), Write(labels))

        def normal_pdf(x):
            m, s = self.mean, self.std
            return (1.0/(np.sqrt(2*np.pi)*s)) * np.exp(-0.5*((x-m)/s)**2)

        graph = axes.plot(normal_pdf, x_range=[self.x_min, self.x_max], color=BLUE)
        self.play(Create(graph))
        self.wait(1)

SCENE_CLASS = NormalDistributionScene
