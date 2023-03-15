// eslint-disable-next-line import/extensions
import { renderOntoNode } from "../dist/index.js";

document.addEventListener("DOMContentLoaded", () => {
  const div = document.querySelector("div.dagred3");
  const graph = renderOntoNode(div);
  graph.setNode("test", { label: "test" });
});
