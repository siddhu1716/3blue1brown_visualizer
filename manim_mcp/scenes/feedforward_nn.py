from typing import Dict, Any, List
from manim import Scene, VGroup, Dot, Line, MathTex, Create, FadeIn, FadeOut, BLUE, YELLOW, WHITE

SCENE_KEY = "feedforward_nn"
PARAM_SCHEMA: Dict[str, Any] = {
    "layers": "List[int]: e.g. [3,4,2]",
    "activation": "str in {'relu','sigmoid','tanh','linear'} (default 'relu')",
}

LAYER_X_SPACING = 2.5
NODE_Y_SPACING = 0.8

class FeedForwardNNScene(Scene):
    def __init__(self, layers: List[int] | None = None, activation: str = "relu", **kwargs):
        super().__init__(**kwargs)
        self.layers = layers or [3, 4, 2]
        self.activation = activation

    def construct(self):
        # Create nodes
        layer_groups: List[VGroup] = []
        for li, n in enumerate(self.layers):
            g = VGroup(*[Dot(radius=0.12, color=WHITE) for _ in range(n)])
            g.arrange(DOWN, buff=NODE_Y_SPACING)
            g.move_to((li * LAYER_X_SPACING - (len(self.layers)-1)*LAYER_X_SPACING/2, 0, 0))
            layer_groups.append(g)
        nodes = VGroup(*layer_groups)
        self.play(Create(nodes))

        # Create connections
        edges = VGroup()
        for li in range(len(layer_groups)-1):
            A, B = layer_groups[li], layer_groups[li+1]
            for a in A:
                for b in B:
                    edges.add(Line(a.get_center(), b.get_center(), stroke_opacity=0.6))
        self.play(Create(edges))

        # Title / activation
        title = MathTex(f"\\text{{Activation:}}\\ {self.activation.upper()}").to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)

SCENE_CLASS = FeedForwardNNScene
