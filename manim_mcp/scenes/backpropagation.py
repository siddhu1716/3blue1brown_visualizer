from typing import Dict, Any, List
import numpy as np
from manim import Scene, VGroup, Dot, Line, MathTex, Create, FadeIn, FadeOut, RED, BLUE, YELLOW, WHITE

SCENE_KEY = "backpropagation"
PARAM_SCHEMA: Dict[str, Any] = {
    "layers": "List[int]: e.g. [3,4,2]",
    "learning_rate": "float (default 0.1)",
}

LAYER_X_SPACING = 2.5
NODE_Y_SPACING = 0.8

class BackpropagationScene(Scene):
    def __init__(self, layers: List[int] | None = None, learning_rate: float = 0.1, **kwargs):
        super().__init__(**kwargs)
        self.layers = layers or [3, 4, 2]
        self.lr = float(learning_rate)

    def construct(self):
        # Nodes
        layer_groups: List[VGroup] = []
        for li, n in enumerate(self.layers):
            g = VGroup(*[Dot(radius=0.12, color=WHITE) for _ in range(n)])
            g.arrange(DOWN, buff=NODE_Y_SPACING)
            g.move_to((li * LAYER_X_SPACING - (len(self.layers)-1)*LAYER_X_SPACING/2, 0, 0))
            layer_groups.append(g)
        nodes = VGroup(*layer_groups)
        self.play(Create(nodes))

        # Forward edges
        f_edges = VGroup()
        for li in range(len(layer_groups)-1):
            A, B = layer_groups[li], layer_groups[li+1]
            for a in A:
                for b in B:
                    f_edges.add(Line(a.get_center(), b.get_center(), stroke_opacity=0.6, color=BLUE))
        self.play(Create(f_edges))

        # Forward pass label
        f_label = MathTex("\\text{Forward Pass}").to_edge(UP)
        self.play(FadeIn(f_label))
        self.wait(0.5)
        self.play(FadeOut(f_label))

        # Backward edges (reverse direction, red)
        b_edges = VGroup()
        for li in range(len(layer_groups)-1, 0, -1):
            A, B = layer_groups[li-1], layer_groups[li]
            for a in A:
                for b in B:
                    b_edges.add(Line(b.get_center(), a.get_center(), stroke_opacity=0.6, color=RED))
        b_label = MathTex("\\text{Backward Pass (gradients)}").to_edge(UP)
        self.play(FadeIn(b_label))
        self.play(Create(b_edges))
        self.wait(1)

SCENE_CLASS = BackpropagationScene
