import { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import layout from "./layout.json";
import useScrollZoom from "../hooks/useScrollZoom";
import Layer from "./Layer/Layer";
import { defaultPointConfig } from "../helpers/configs";
import InfoBox from "./InfoBox/InfoBox";

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
  infoBox: {
    position: "fixed",
    top: theme.spacing(10),
    right: theme.spacing(8)
  }
}));

export default function Simulation({ settings, children }) {
  const classes = useStyles();
  const scale = useScrollZoom(0.4);
  const [selectedElement, setSelectedElement] = useState(null);

  const selectElement = (element) => {
    setSelectedElement(element);
  };

  const clearElement = () => {
    setSelectedElement(null);
  };

  const clipPath = `polygon(${layout.contour.reduce((acc, point, index) => {
    return (
      acc +
      `${point[0]}px ${point[1]}px` +
      (index !== layout.contour.length - 1 ? ", " : "")
    );
  }, "")})`;
  const translateWidth = (layout["image-size"][0] * (1 - scale)) / 2;
  const translateHeight = (layout["image-size"][1] * (1 - scale)) / 2;
  return (
    <div className={classes.root} style={{}}>
      <div
        className={classes.layout}
        style={{
          transform: `translate(-${Math.max(
            0,
            parseInt(translateWidth)
          )}px, -${Math.max(0, parseInt(translateHeight))}px) scale(${Number(
            scale
          ).toFixed(1)})`,
          clipPath: clipPath,
          width: layout["image-size"][0],
          height: layout["image-size"][1],
        }}
      >
        {Object.entries(layout.objects).map(([name, objDef]) => (
          <Layer
            key={name}
            settings={{name, elements: objDef.ids.length}}
            points={objDef.points}
            ids={objDef.ids}
            onElementClick={selectElement}
            config={{
              ...defaultPointConfig,
              color: objDef.color,
              fill: objDef.fill,
            }}
          />
        ))}
        {Object.entries(layout.items).map(([name, objDef]) => (
          <Layer
            key={name}
            settings={{name, elements: objDef.ids.length}}
            points={objDef.points}
            ids={objDef.ids}
            onElementClick={selectElement}
            config={{
              ...defaultPointConfig,
              color: objDef.color,
              fill: objDef.fill,
            }}
          />
        ))}
      </div>
      {selectedElement != null && (
        <InfoBox
          className={classes.infoBox}
          title={selectedElement.name}
          message={selectedElement.message}
          position={selectedElement.position}
          onClose={clearElement}
          color={selectedElement.color}
        />
      )}
    </div>
  );
}
