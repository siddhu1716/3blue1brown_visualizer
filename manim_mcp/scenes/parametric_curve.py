from typing import Dict, Any
import numpy as np
from manim import Scene, Axes, ParametricFunction, Create, MathTex, BLUE

SCENE_KEY = "parametric_curve"
PARAM_SCHEMA: Dict[str, Any] = {
    "x_of_t": "str: x(t), e.g. 'cos(t)'",
    "y_of_t": "str: y(t), e.g. 'sin(t)'",
    "t_min": "float (default 0)",
    "t_max": "float (default 2*pi)",
    "color": "str/color (default BLUE)",
}

SAFE_NS = {
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

class ParametricCurveScene(Scene):
    def __init__(self,
                 x_of_t: str = "cos(t)",
                 y_of_t: str = "sin(t)",
                 t_min: float = 0.0,
                 t_max: float = 2*np.pi,
                 color: Any = BLUE,
                 **kwargs):
        super().__init__(**kwargs)
        self.x_of_t = x_of_t
        self.y_of_t = y_of_t
        self.t_min = float(t_min)
        self.t_max = float(t_max)
        self.color = color

    def construct(self):
        axes = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=8, y_length=8)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(Create(axes), Create(labels))

        def x(t):
            return eval(self.x_of_t, {"__builtins__": {}}, {**SAFE_NS, "t": t})

        def y(t):
            return eval(self.y_of_t, {"__builtins__": {}}, {**SAFE_NS, "t": t})

        curve = ParametricFunction(lambda t: axes.c2p(x(t), y(t)), t_range=[self.t_min, self.t_max], color=self.color or BLUE)
        self.play(Create(curve))
        self.wait(1)

SCENE_CLASS = ParametricCurveScene
