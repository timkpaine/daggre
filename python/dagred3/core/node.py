from dagred3 import BaseModel, Field, PrivateAttr

from .common import Color, Graph, Shape


class Node(BaseModel):
    shape: Shape = "rect"
    tooltip: str = ""
    color: Color = Field(default=Color("black"))
    backgroundColor: Color = Field(default=Color("rgba(255, 255, 255, 0)"))

    _graph: Graph = PrivateAttr(None)  # type: ignore[valid-type]

    def _setGraph(self, graph: Graph):  # type: ignore[valid-type]
        self._graph = graph

    def __eq__(self, other: object) -> bool:
        # for identity
        if isinstance(other, Node):
            return self.id == other.id
        raise TypeError(f"Unsupported operation `==` between Node and {type(other)}")

    def __lt__(self, other: object) -> bool:
        # for sorting
        if isinstance(other, Node):
            return self.name < other.name
        raise TypeError(f"Unsupported operation `<` between Node and {type(other)}")

    def __repr__(self) -> str:
        return f"Node[{self.name or self.id[:10]}]"
