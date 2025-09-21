from typing import Dict, Any
import numpy as np
from manim import ThreeDScene, ThreeDAxes, Surface, MathTex, Create, Write, BLUE, YELLOW

SCENE_KEY = "loss_landscape"
PARAM_SCHEMA: Dict[str, Any] = {
    "function": "str: z=f(x,y) (default '(x-1)**2 + (y+2)**2')",
    "x_range": "List[float]: [min,max,step] (default [-3,3,1])",
    "y_range": "List[float]: [min,max,step] (default [-3,3,1])",
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

class LossLandscapeScene(ThreeDScene):
    def __init__(self, function: str = "(x-1)**2 + (y+2)**2", x_range=None, y_range=None, **kwargs):
        super().__init__(**kwargs)
        self.function = function
        self.x_range = x_range or [-3, 3, 1]
        self.y_range = y_range or [-3, 3, 1]

    def f(self, x, y):
        return eval(self.function, {"__builtins__": {}}, {**SAFE_NS, "x": x, "y": y})

    def construct(self):
        axes = ThreeDAxes(x_range=self.x_range, y_range=self.y_range, z_range=[0, 20, 5])
        title = MathTex("\\text{Loss Landscape}").to_edge(UP)
        self.play(Write(title))
        self.play(Create(axes))

        def surf(u, v):
            x = u
            y = v
            z = self.f(x, y)
            return axes.c2p(x, y, z)

        surface = Surface(
            lambda u, v: surf(u, v),
            u_range=(self.x_range[0], self.x_range[1]),
            v_range=(self.y_range[0], self.y_range[1]),
            resolution=(24, 24),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE, YELLOW],
        )
        self.play(Create(surface))
        self.set_camera_orientation(phi=60 * np.pi / 180, theta=45 * np.pi / 180, zoom=1.0)
        self.wait(1)

SCENE_CLASS = LossLandscapeScene
