/* eslint-disable no-param-reassign */
import { graphlib, render } from "dagre-d3-es";
import * as d3 from "d3";

// Arrowheads - "normal", "vee", "undirected"
// Curves - https://github.com/d3/d3-shape/blob/v3.2.0/README.md#curveBasis

// g.setNode(id, {
//   labelType: "html",
//   label: html,
//   rx: 5,
//   ry: 5,
//   padding: 0,
//   class: className
// });

// https://github.com/dagrejs/dagre/blob/master/lib/layout.js
// rankdir: ["tb", "bt", "lr", "rl"]

const _directionToShorthand = (direction) => {
  switch ((direction || "tb").toLowerCase()) {
    case undefined:
    case "top-to-bottom":
      return "TB";
    case "bottom-to-top":
      return "BT";
    case "left-to-right":
      return "LR";
    case "right-to-left":
      return "RL";
    default:
      return direction;
  }
};

const _configureDefaults = (options) => {
  const defaults = options || {};
  // Graph defaults
  defaults.initialScale = options.initialScale || 1.0;
  defaults.directed = options.directed || true;
  defaults.nodesep = options.nodesep || 70;
  defaults.ranksep = options.ranksep || 50;
  defaults.rankdir = _directionToShorthand(options.direction);
  defaults.marginx = options.marginx || 20;
  defaults.marginy = options.marginy || 20;

  // Node defaults
  defaults.node = defaults.node || {};
  defaults.node.style = defaults.node.style || "";
  // defaults.node.defaultLabel = undefined;

  // Edge defaults
  defaults.edge = defaults.edge || {};
  defaults.edge.curve = options.edge?.curve || d3.curveBasis;
  defaults.edge.arrowheadClass =
    options.edge?.arrowheadClass || "dagre-d3-arrowhead";
  defaults.edge.arrowheadStyle = options.edge?.arrowheadStyle || "fill: #333;";
  defaults.edge.style = options.edge?.style || "stroke: #333;stroke-width:1px;";
  // defaults.edge.defaultLabel = undefined;

  // Other defaults
  return defaults;
};

const _configureNodeDefaults = (name, options, defaults) => {
  const resolvedOptions = { ...defaults, ...options };

  if (!resolvedOptions.label) {
    resolvedOptions.label = defaults.defaultLabel || name;
  }
  if (resolvedOptions.color) {
    resolvedOptions.labelStyle = `${resolvedOptions.style} fill: ${resolvedOptions.color};`;
  }
  if (resolvedOptions.backgroundColor) {
    resolvedOptions.style = `${resolvedOptions.style} fill: ${resolvedOptions.backgroundColor};`;
  }

  return resolvedOptions;
};

const _configureEdgeDefaults = (from, to, options, defaults) => {
  const resolvedOptions = { ...defaults, ...options };

  if (resolvedOptions.line === "dash") {
    resolvedOptions.style = `${resolvedOptions.style}stroke-dasharray: 5, 5;`;
  }
  return resolvedOptions;
};

export class Graph {
  constructor(options = {}) {
    // parse out options
    this._defaults = _configureDefaults(options);

    // create renderer
    this._renderer = render();

    // create graph
    this._graph = new graphlib.Graph({ directed: this._defaults.directed });

    // intiialize graph
    this._graph.setGraph({
      nodesep: this._defaults.nodesep,
      ranksep: this._defaults.ranksep,
      rankdir: this._defaults.rankdir,
      marginx: this._defaults.marginx,
      marginy: this._defaults.marginy,
    });
    this._graph.setDefaultEdgeLabel(() => {});

    // setup flags
    this._rendered = false;

    // vars for svg elements
    this._graph_svg_inst = null;
    this._graph_g_inst = null;

    // bind methods
    this.addNode.bind(this);
    this.addEdge.bind(this);
    this.render.bind(this);
    this._calculateInitialScale.bind(this);
  }

  addNode(name, options = {}) {
    this._graph.setNode(
      name,
      _configureNodeDefaults(name, options, this._defaults.node),
    );
  }

  addEdge(from, to, options = {}) {
    this._graph.setEdge(
      from,
      to,
      _configureEdgeDefaults(from, to, options, this._defaults.edge),
    );
  }

  render(onto) {
    if (!this._rendered) {
      // add class to `onto`
      onto.classList.add("dagred3-container");

      // create svg and g elements
      this._graph_svg_inst = d3.select(onto).append("svg");
      this._graph_g_inst = this._graph_svg_inst.append("g");

      // setup zoom
      this._zoom = d3.zoom().on("zoom", (event) => {
        this._graph_g_inst.attr("transform", event.transform);
      });
      this._graph_svg_inst.call(this._zoom);
    }

    // render
    this._renderer(this._graph_g_inst, this._graph);

    if (!this._rendered) {
      // scale initial view
      // calculate initial scale modifier
      this._calculateInitialScale();

      const width = onto.offsetWidth;
      const height = onto.offsetHeight;
      this._graph_svg_inst.call(
        this._zoom.transform,
        d3.zoomIdentity
          .translate(
            (width - this._graph.graph().width * this._defaults.initialScale) /
              2,
            (height -
              this._graph.graph().height * this._defaults.initialScale) /
              2,
          )
          .scale(this._defaults.initialScale),
      );
    }

    // mark as initially rendered
    this._rendered = true;
  }

  _calculateInitialScale() {
    if (this._defaults.initialScale === undefined) {
      this._defaults.initialScale = 1.0;
    }

    // calculate initial scale as function of number of nodes / edges
    // TODO
    console.log(
      `Scale count: ${this._graph.edgeCount() + this._graph.nodeCount()}`,
    );
    if (this._graph.edgeCount() + this._graph.nodeCount() < 10) {
      this._defaults.initialScale *= 4;
    } else if (this._graph.edgeCount() + this._graph.nodeCount() < 20) {
      this._defaults.initialScale *= 3;
    } else if (this._graph.edgeCount() + this._graph.nodeCount() < 40) {
      this._defaults.initialScale *= 2;
    } else if (this._graph.edgeCount() + this._graph.nodeCount() < 80) {
      this._defaults.initialScale *= 1;
    } else if (this._graph.edgeCount() + this._graph.nodeCount() < 100) {
      this._defaults.initialScale *= 0.5;
    } else if (this._graph.edgeCount() + this._graph.nodeCount() < 500) {
      this._defaults.initialScale *= 0.25;
    } else {
      this._defaults.initialScale *= 0.1;
    }
  }
}
