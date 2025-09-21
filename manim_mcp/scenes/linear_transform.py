from typing import Dict, Any, List
import numpy as np
from manim import Scene, NumberPlane, Vector, VGroup, Matrix, MathTex, FadeIn, Transform, Create, BLUE, YELLOW, WHITE

SCENE_KEY = "linear_transform"
PARAM_SCHEMA: Dict[str, Any] = {
    "matrix": "List[List[float]]: 2x2 matrix, e.g. [[1,0],[0,1]]",
    "show_basis": "bool (default True)",
    "grid_x_range": "List[float]: [min, max, step] (default [-6, 6, 1])",
    "grid_y_range": "List[float]: [min, max, step] (default [-4, 4, 1])",
}

class LinearTransformScene(Scene):
    def __init__(self,
                 matrix: List[List[float]] | None = None,
                 show_basis: bool = True,
                 grid_x_range: List[float] | None = None,
                 grid_y_range: List[float] | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.M = np.array(matrix if matrix is not None else [[1.0, 0.0], [0.0, 1.0]], dtype=float)
        self.show_basis = bool(show_basis)
        self.grid_x_range = grid_x_range or [-6, 6, 1]
        self.grid_y_range = grid_y_range or [-4, 4, 1]

    def construct(self):
        plane = NumberPlane(x_range=self.grid_x_range, y_range=self.grid_y_range)
        self.play(Create(plane))

        vectors = VGroup()
        e1 = Vector([1, 0], color=BLUE)
        e2 = Vector([0, 1], color=YELLOW)
        if self.show_basis:
            vectors.add(e1, e2)
            self.play(Create(vectors))

        # Show matrix label
        mat_label = Matrix(self.M.round(2).tolist())
        mat_label.to_corner()
        self.play(FadeIn(mat_label))

        # Apply linear transform to the plane and basis
        self.play(Transform(plane, plane.apply_matrix(self.M)))
        if self.show_basis:
            e1_t = Vector((self.M @ np.array([1, 0], dtype=float)).tolist(), color=BLUE)
            e2_t = Vector((self.M @ np.array([0, 1], dtype=float)).tolist(), color=YELLOW)
            self.play(Transform(vectors[0], e1_t), Transform(vectors[1], e2_t))
        self.wait(1)

SCENE_CLASS = LinearTransformScene
