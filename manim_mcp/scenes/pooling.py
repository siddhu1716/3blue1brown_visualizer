from typing import Dict, Any
import numpy as np
from manim import Scene, Matrix, SurroundingRectangle, VGroup, Create, Transform, MathTex, YELLOW

SCENE_KEY = "pooling"
PARAM_SCHEMA: Dict[str, Any] = {
    "pool_type": "str in {'max','avg'} (default 'max')",
    "kernel_size": "int (default 2)",
    "stride": "int (default equals kernel_size)",
    "input_matrix": "List[List[float]] (default 4x4 sample)",
}

DEFAULT_INPUT = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [2, 2, 9, 1],
    [0, 3, 1, 5],
]

class PoolingScene(Scene):
    def __init__(self,
                 pool_type: str = "max",
                 kernel_size: int = 2,
                 stride: int | None = None,
                 input_matrix = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.pool_type = (pool_type or "max").lower()
        self.k = int(kernel_size)
        self.s = int(stride) if stride is not None else int(kernel_size)
        self.X = np.array(input_matrix if input_matrix is not None else DEFAULT_INPUT, dtype=float)

    def construct(self):
        X_m = Matrix(self.X.tolist()).scale(0.7).to_edge(LEFT)
        self.play(Create(X_m))

        H, W = self.X.shape
        out_h = (H - self.k) // self.s + 1
        out_w = (W - self.k) // self.s + 1
        Y = np.zeros((out_h, out_w))
        Y_m = Matrix(Y.tolist()).scale(0.7).next_to(X_m, RIGHT, buff=1.5)
        title = MathTex(self.pool_type.upper() + "\\ Pooling").to_edge(UP)
        self.play(Create(title), Create(Y_m))

        rect = SurroundingRectangle(X_m.get_entries()[0], color=YELLOW)
        self.add(rect)

        for i in range(out_h):
            for j in range(out_w):
                r0 = i * self.s
                c0 = j * self.s
                window_entries = []
                for r in range(self.k):
                    for c in range(self.k):
                        idx = r0 * X_m.ncols + c0 + r * X_m.ncols + c
                        window_entries.append(X_m.get_entries()[idx])
                new_rect = SurroundingRectangle(VGroup(*window_entries), color=YELLOW)
                self.play(Transform(rect, new_rect))

                patch = self.X[r0:r0+self.k, c0:c0+self.k]
                val = float(np.max(patch)) if self.pool_type == "max" else float(np.mean(patch))
                Y[i, j] = val
                out_idx = i * Y_m.ncols + j
                self.play(Transform(Y_m.get_entries()[out_idx], MathTex(f"{val:.1f}").scale(0.6)))

        self.wait(1)

SCENE_CLASS = PoolingScene
