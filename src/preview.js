import { renderOntoNode } from "./index";

document.addEventListener("DOMContentLoaded", () => {
  const div = document.querySelector("div.dagred3");
  const graph = renderOntoNode(div);
  graph.setNode("test", { label: "test" });
});
