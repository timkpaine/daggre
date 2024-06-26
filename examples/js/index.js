// eslint-disable-next-line import/no-extraneous-dependencies
import { Graph } from "daggre";

const SCALE = 10;

document.addEventListener("DOMContentLoaded", () => {
  const div = document.querySelector("div.daggre");
  const graph = new Graph({ direction: "left-to-right" });

  let begin = 0;

  const build = () => {
    for (let i = begin; i < begin + SCALE; i += 1) {
      if (i > 0) {
        if (i % 2 === 0) {
          graph.addNode(`test${i}`, { color: "red" });
        } else {
          graph.addNode(`test${i}`, {
            shape: "ellipse",
            backgroundColor: "lightblue",
          });
        }
        graph.addEdge(`test${i - 1}`, `test${i}`);
      } else {
        graph.addNode(`test${i}`, {
          shape: "house",
          backgroundColor: "lightgreen",
        });
      }

      if (i > 2) {
        Array(4)
          .fill(0)
          .forEach((_, j) => {
            if (i % (j + 2) === 0) {
              graph.addEdge(`test${i / (j + 2)}`, `test${i}`, {
                arrowhead: "hollowpoint",
                line: "dash",
              });
            }
          });
      }
    }
    graph.render(div);
    begin += SCALE;
  };
  build();
  // setInterval(build, 5000);
});
