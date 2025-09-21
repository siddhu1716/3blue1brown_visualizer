from typing import Dict, Any
import numpy as np
from manim import Scene, Axes, MathTex, Create, Write, BLUE, YELLOW

SCENE_KEY = "activation_function"
PARAM_SCHEMA: Dict[str, Any] = {
    "function": "str in {'sigmoid','relu','tanh'} (default 'sigmoid')",
    "x_min": "float (default -6)",
    "x_max": "float (default 6)",
}

FUNC_MAP = {
    "sigmoid": lambda x: 1.0 / (1.0 + np.exp(-x)),
    "relu": lambda x: np.maximum(0.0, x),
    "tanh": lambda x: np.tanh(x),
}

class ActivationFunctionScene(Scene):
    def __init__(self, function: str = "sigmoid", x_min: float = -6.0, x_max: float = 6.0, **kwargs):
        super().__init__(**kwargs)
        self.function = (function or "sigmoid").lower()
        self.x_min = float(x_min)
        self.x_max = float(x_max)

    def construct(self):
        axes = Axes(x_range=[self.x_min, self.x_max, (self.x_max-self.x_min)/4], y_range=[-1.5, 1.5, 0.5], x_length=10, y_length=4)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("f(x)"))
        self.play(Create(axes), Write(labels))

        f = FUNC_MAP.get(self.function, FUNC_MAP["sigmoid"])
        graph = axes.plot(f, x_range=[self.x_min, self.x_max], color=BLUE)
        title = MathTex(self.function.upper()).to_edge(UP)
        self.play(Write(title), Create(graph))
        self.wait(1)

SCENE_CLASS = ActivationFunctionScene
