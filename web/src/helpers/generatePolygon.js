import { defaultPointConfig } from "./configs";

export default function generatePolygon(
  points = [],
  config = defaultPointConfig
) {
  const { color, border, borderWidth, fill } = config;
  const minX = Math.min(...points.map((point) => point[0]));
  const maxX = Math.max(...points.map((point) => point[0]));
  const minY = Math.min(...points.map((point) => point[1]));
  const maxY = Math.max(...points.map((point) => point[1]));

  const style = {
    fill: color,
    stroke: border,
    strokeWidth: borderWidth,
    fillRule: fill ? "nonzero" : "evenodd",
  };
  const modPoints = points
    .map((point) => [point[0] - minX, point[1] - minY].join(","))
    .join(" ");
  return {
    position: {
      minX: minX,
      minY: minY,
      maxX: maxX,
      maxY: maxY,
    },
    points: modPoints,
    style: style,
  };
}
