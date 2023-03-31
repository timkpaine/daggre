from typing import ForwardRef, Literal
from pydantic.color import Color  # noqa: F401

# Forward references
Graph = ForwardRef("Graph")

# Graph
Direction = Literal["left-to-right", "right-to-left", "top-to-bottom", "bottom-to-top"]

# Edge
Arrowhead = Literal["normal", "vee", "undirected"]
LabelPosition = Literal["r", "c", "l"]
Line = Literal["solid", "dash"]

# Node
Shape = Literal["rect", "circle", "ellipse", "diamond"]
