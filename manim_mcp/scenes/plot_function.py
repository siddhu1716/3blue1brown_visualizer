from typing import Dict, Any
import numpy as np
from manim import Scene, Axes, MathTex, Create, Write, BLUE, YELLOW

SCENE_KEY = "plot_function"
PARAM_SCHEMA: Dict[str, Any] = {
    "expression": "str: function of x, e.g. 'sin(x) + 0.5*cos(2*x)'",
    "x_min": "float (default 0)",
    "x_max": "float (default 2*pi)",
    "color": "str/color (default BLUE)",
}

SAFE_NS = {
    # numpy functions
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "pi": np.pi,
    "e": np.e,
    "abs": np.abs,
}

class PlotFunctionScene(Scene):
    def __init__(self, expression: str = "sin(x)", x_min: float = 0.0, x_max: float = 2*np.pi, color: Any = BLUE, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression
        self.x_min = float(x_min)
        self.x_max = float(x_max)
        self.color = color

    def construct(self):
        axes = Axes(x_range=[self.x_min, self.x_max, (self.x_max - self.x_min)/4], y_range=[-2, 2, 1], x_length=10, y_length=4)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("f(x)"))
        self.play(Create(axes), Write(labels))

        def f(x):
            local = {"x": x}
            return eval(self.expression, {"__builtins__": {}}, {**SAFE_NS, **local})

        graph = axes.plot(f, x_range=[self.x_min, self.x_max], color=self.color or BLUE)
        self.play(Create(graph))
        self.wait(1)

SCENE_CLASS = PlotFunctionScene
