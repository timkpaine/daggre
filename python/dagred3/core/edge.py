from typing import Optional

from ..transports import BaseModel, PrivateAttr
from .common import Arrowhead, Graph, LabelPosition, Line
from .node import Node


class Edge(BaseModel):
    from_: Node
    to_: Node
    tooltip: str = ""
    line: Line = "solid"
    labelposition: LabelPosition = "r"
    labeloffset: Optional[float] = None
    arrowhead: Arrowhead = "vee"

    _graph: Graph = PrivateAttr(None)  # type: ignore[valid-type]

    def _setGraph(self, graph: Graph):  # type: ignore[valid-type]
        self._graph = graph

    def __lt__(self, other):
        return self.from_.name < other.from_.name or self.to_.name < other.to_.name

    def __repr__(self) -> str:
        return f"Edge[{self.from_.name} -> {self.to_.name}]"
