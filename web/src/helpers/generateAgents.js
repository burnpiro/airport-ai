import { defaultPointConfig } from "./configs";

export default function generateAgents(
  points = [],
  config = defaultPointConfig
) {
  const { color, border, borderWidth, fill } = config;

  return points.map((point) => ({
    position: {
      x: point.x,
      y: point.y,
    },
    id: point.id,
    size: 50,
    style: {
      color: color,
      fill: fill ? color : "transparent",
      stroke: fill ? border : color,
      strokeWidth: borderWidth,
      fillRule: fill ? "nonzero" : "evenodd",
    },
  }));
}
