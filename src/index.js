import { render, graphlib } from "dagre-d3-es";
import * as d3 from "d3";

import "./index.css";

export const renderOntoNode = (div) => {
  const { Graph } = graphlib;
  const graph = new Graph().setGraph({ height: 400, width: 400 });

  // eslint-disable-next-line new-cap
  const renderer = new render();

  const svg = d3.select(div).append("svg");
  svg.attr("height", 600);
  svg.attr("width", 600);

  const g = svg.append("g");
  g.attr("height", 600);
  g.attr("width", 600);

  graph.setNode("test", { label: "test" });
  graph.setNode("test2", { label: "test2" });
  graph.setEdge("test", "test2", { label: "" });
  renderer(g, graph);
  return graph;
};

export const thing = "test";
