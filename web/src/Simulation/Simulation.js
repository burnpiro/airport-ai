import { makeStyles } from "@material-ui/core/styles";
import layout from "./layout.json";
import useScrollZoom from "../hooks/useScrollZoom";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    height: "100%",
    overflow: "scroll",
    position: "relative",
  },
  layout: {
    backgroundColor: "#fff1b8",
    position: "relative",
    maxWidth: "none",
  },
}));

export default function Simulation({ settings, children }) {
  const classes = useStyles();
  const scale = useScrollZoom(0.4)

  const clipPath = `polygon(${layout.contour.reduce((acc, point, index) => {
    return (
      acc +
      `${point[0]}px ${point[1]}px` +
      (index !== layout.contour.length - 1 ? ", " : "")
    );
  }, "")})`;
  const translateWidth = layout["image-size"][0]*(1-scale)/2;
  const translateHeight = layout["image-size"][1]*(1-scale)/2;
  return (
    <div className={classes.root} style={{}}>
      <div
        className={classes.layout}
        style={{
          transform: `scale(${scale}) translate(-${translateWidth}px, -${translateHeight}px)`,
          clipPath: clipPath,
          width: layout["image-size"][0],
          height: layout["image-size"][1],
        }}
      />
    </div>
  );
}
