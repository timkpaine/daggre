import { intersect } from "dagre-d3-es";

export const house = (parent, bbox, node) => {
  const w = bbox.width;
  const h = bbox.height;
  const points = [
    { x: 0, y: 0 },
    { x: w, y: 0 },
    { x: w, y: -h },
    { x: w / 2, y: (-h * 3) / 2 },
    { x: 0, y: -h },
  ];

  const shapeSvg = parent
    .insert("polygon", ":first-child")
    .attr("points", points.map((d) => `${d.x},${d.y}`).join(" "))
    .attr("transform", `translate(${-w / 2},${(h * 3) / 4})`);

  // eslint-disable-next-line no-param-reassign
  node.intersect = (point) => intersect.polygon(node, points, point);

  return shapeSvg;
};
