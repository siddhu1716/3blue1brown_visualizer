from typing import Dict, Any, List
import numpy as np
from manim import Scene, VGroup, Square, Integer, Matrix, SurroundingRectangle, Create, FadeIn, Transform, YELLOW, BLUE, GREEN

SCENE_KEY = "convolution"
PARAM_SCHEMA: Dict[str, Any] = {
    "input_matrix": "List[List[float]] (default 5x5 sample)",
    "kernel": "List[List[float]] (default 3x3 edge detector)",
    "stride": "int (default 1)",
}

DEFAULT_INPUT = [
    [1, 2, 3, 2, 1],
    [0, 1, 2, 1, 0],
    [1, 2, 4, 2, 1],
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
]

DEFAULT_KERNEL = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1],
]

class ConvolutionScene(Scene):
    def __init__(self,
                 input_matrix: List[List[float]] | None = None,
                 kernel: List[List[float]] | None = None,
                 stride: int = 1,
                 **kwargs):
        super().__init__(**kwargs)
        self.X = np.array(input_matrix if input_matrix is not None else DEFAULT_INPUT, dtype=float)
        self.K = np.array(kernel if kernel is not None else DEFAULT_KERNEL, dtype=float)
        self.stride = int(stride)

    def construct(self):
        # Display input and kernel as Matrix mobjects for clarity
        X_m = Matrix(self.X.tolist()).scale(0.6).to_edge(LEFT)
        K_m = Matrix(self.K.tolist()).scale(0.6).next_to(X_m, RIGHT, buff=1.2)
        self.play(Create(X_m), Create(K_m))

        kh, kw = self.K.shape
        H, W = self.X.shape
        out_h = (H - kh) // self.stride + 1
        out_w = (W - kw) // self.stride + 1
        Y = np.zeros((out_h, out_w))
        Y_m = Matrix(Y.tolist()).scale(0.6).next_to(K_m, RIGHT, buff=1.2)
        self.play(Create(Y_m))

        # Sliding window visualization with a rectangle
        rect = SurroundingRectangle(X_m.get_entries()[0], color=YELLOW)
        self.add(rect)

        idx = 0
        for i in range(out_h):
            for j in range(out_w):
                # compute top-left index in input
                r0 = i * self.stride
                c0 = j * self.stride
                # entries in the kxk window
                window_entries = []
                for r in range(kh):
                    for c in range(kw):
                        idx_in_matrix = r0 * X_m.ncols + c0 + r * X_m.ncols + c
                        window_entries.append(X_m.get_entries()[idx_in_matrix])
                new_rect = SurroundingRectangle(VGroup(*window_entries), color=YELLOW)
                self.play(Transform(rect, new_rect))

                val = float(np.sum(self.X[r0:r0+kh, c0:c0+kw] * self.K))
                Y[i, j] = val
                # Update output entry
                out_idx = i * Y_m.ncols + j
                self.play(Transform(Y_m.get_entries()[out_idx], Integer(int(round(val))).scale(0.6)))

        self.wait(1)

SCENE_CLASS = ConvolutionScene
