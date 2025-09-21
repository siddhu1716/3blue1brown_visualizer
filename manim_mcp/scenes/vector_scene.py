from typing import Dict, Any, List
import numpy as np
from manim import Scene, NumberPlane, Vector, VGroup, Dot, Line, MathTex, Create, FadeIn, Transform, BLUE, YELLOW, WHITE, RED, RIGHT

SCENE_KEY = "vector"
PARAM_SCHEMA: Dict[str, Any] = {
    "vectors": "List[List[float]]: list of 2D vectors",
    "colors": "List[str]: optional list of manim color names",
}

COLOR_MAP = [BLUE, YELLOW, WHITE, RED]

class VectorScene(Scene):
    def __init__(self, vectors: List[List[float]] | None = None, colors: List[str] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.vectors = vectors or [[2, 1], [-1, 2]]
        self.colors = colors or []

    def construct(self):
        plane = NumberPlane()
        self.play(Create(plane))

        vgroup = VGroup()
        for i, v in enumerate(self.vectors):
            col = COLOR_MAP[i % len(COLOR_MAP)]
            vec = Vector(v, color=col)
            vgroup.add(vec)
        self.play(Create(vgroup))

        if len(self.vectors) >= 2:
            a = np.array(self.vectors[0], dtype=float)
            b = np.array(self.vectors[1], dtype=float)
            sum_vec = Vector((a + b).tolist(), color=RED)
            plus = MathTex("+").next_to(Vector(a).get_end(), RIGHT)
            eq = MathTex("=")
            self.play(Create(sum_vec))
        self.wait(1)

SCENE_CLASS = VectorScene
