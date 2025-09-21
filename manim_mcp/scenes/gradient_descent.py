from typing import Dict, Any, Tuple
import numpy as np
from manim import Scene, Axes, Dot, Vector, VGroup, MathTex, Create, Write, FadeIn, FadeOut, RED, BLUE

SCENE_KEY = "gradient_descent"
PARAM_SCHEMA: Dict[str, Any] = {
    "function": "str: f(x,y) in terms of x,y, e.g. '(x-1)**2 + (y+2)**2'",
    "start_point": "List[float]: [x0,y0] (default [3,3])",
    "learning_rate": "float (default 0.1)",
    "steps": "int (default 20)",
    "x_range": "List[float]: [min,max,step] (default [-4,4,1])",
    "y_range": "List[float]: [min,max,step] (default [-4,4,1])",
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

class GradientDescentScene(Scene):
    def __init__(self,
                 function: str = "(x-1)**2 + (y+2)**2",
                 start_point: Tuple[float, float] | None = None,
                 learning_rate: float = 0.1,
                 steps: int = 20,
                 x_range = None,
                 y_range = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.function = function
        self.p = np.array(start_point or [3.0, 3.0], dtype=float)
        self.lr = float(learning_rate)
        self.steps = int(steps)
        self.x_range = x_range or [-4, 4, 1]
        self.y_range = y_range or [-4, 4, 1]

    def f(self, x, y):
        return eval(self.function, {"__builtins__": {}}, {**SAFE_NS, "x": x, "y": y})

    def grad(self, x, y, eps: float = 1e-4):
        fx = (self.f(x + eps, y) - self.f(x - eps, y)) / (2*eps)
        fy = (self.f(x, y + eps) - self.f(x, y - eps)) / (2*eps)
        return np.array([fx, fy], dtype=float)

    def construct(self):
        axes = Axes(x_range=self.x_range, y_range=self.y_range, x_length=8, y_length=8)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(Create(axes), Write(labels))

        path_points = [self.p.copy()]
        for _ in range(self.steps):
            g = self.grad(*self.p)
            self.p = self.p - self.lr * g
            path_points.append(self.p.copy())

        dots = VGroup(*[Dot(axes.c2p(px, py), color=RED, radius=0.06) for px, py in path_points])
        self.play(FadeIn(dots[0]))
        for i in range(1, len(dots)):
            self.play(FadeIn(dots[i]))
        self.wait(1)

SCENE_CLASS = GradientDescentScene
