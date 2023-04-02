from typing import Any, Dict, List, Optional, Union, cast
from dagred3 import BaseModel, Field
from .common import Direction
from .edge import Edge
from .exceptions import MalformedArgument
from .node import Node


class Graph(BaseModel):
    directed: bool = True
    multigraph: bool = False
    compound: bool = False
    direction: Direction = "top-to-bottom"
    edges: List[Edge] = Field(default_factory=list)
    nodes: Dict[str, Node] = Field(default_factory=dict)

    def addNode(self, node: Union[str, Node], **node_kwargs: Any) -> Node:
        if isinstance(node, str):
            node_kwargs["name"] = node
            return self.addNode(Node(**node_kwargs))
        elif isinstance(node, Node):
            if node.name in self.nodes:
                # replace with new value
                self.nodes[node.name].onUpdate(node)
            else:
                # assign in
                self.nodes[node.name] = node

                # attach graph to node for convenience
                node._setGraph(self)

            # send to clients
            self.update(model=node, model_target=self.id)

            # return updated
            return self.nodes[node.name]

        # raise if unsupported type
        raise MalformedArgument(f"Bad argument type: {node} {type(node)}")

    def addEdge(self, edge_or_node_from_: Union[str, Edge, Node], to_: Optional[Union[str, Node]] = None, **edge_kwargs) -> None:
        node1: Optional[Node]
        node2: Optional[Node]
        edge: Edge

        if isinstance(edge_or_node_from_, str):
            # get actual node
            node1 = self.addNode(edge_or_node_from_)
        elif isinstance(edge_or_node_from_, Node):
            # use node passed in
            node1 = edge_or_node_from_
        elif isinstance(edge_or_node_from_, Edge):
            # no node1, edge
            node1 = None
            edge = edge_or_node_from_

            # ensure nodes on edge are in graph
            self.addNode(edge_or_node_from_.from_)
            self.addNode(edge_or_node_from_.to_)
        else:
            raise MalformedArgument(f"Bad argument type for `edge_or_node_from_`: {edge_or_node_from_} {type(edge_or_node_from_)}")

        if node1:
            # creating edge from nodes, so grab node2
            if isinstance(to_, str):
                # get actual node
                node2 = self.addNode(to_)
            elif isinstance(to_, Node):
                # use node passed in
                node2 = to_
            else:
                raise MalformedArgument(f"Bad argument type for `to_`: {to_} {type(to_)}")
        else:
            node2 = None

        if node1 and node2:
            # create edge from nodes directly
            edge = Edge(from_=node1, to_=node2, **edge_kwargs)
            self.addEdge(edge)
        else:
            # make mypy happy
            edge = cast(Edge, edge_or_node_from_)

            # TODO check if graph supports multiple edges

            # add edge to list of edges
            self.edges.append(edge)

            # attach graph to edge for convenience
            edge._setGraph(self)

            # send to clients
            self.update(model=edge, model_target=self.id)

    def onUpdate(self, other: Union["Graph", Node, Edge], **kwargs) -> None:  # type: ignore[override]
        if isinstance(other, Node):
            self.addNode(other)
        elif isinstance(other, Edge):
            self.addEdge(other)
        elif isinstance(other, Graph):
            # TODO
            ...
