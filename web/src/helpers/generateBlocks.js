import generatePolygon from "./generatePolygon";
import {defaultPointConfig} from "./configs";

export default function generateBlocks(
  points = [],
  config = defaultPointConfig
) {

  return points.map(pointGroup => generatePolygon(pointGroup, config))
}
