import { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import layout from "./layout.json";
import useScrollZoom from "../hooks/useScrollZoom";
import Layer from "./Layer/Layer";
import { defaultPointConfig } from "../helpers/configs";
import InfoBox from "./InfoBox/InfoBox";
import LayersList from "./LayersList/LayersList";

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
    right: theme.spacing(8),
  },
  layerList: {
    position: "fixed",
    top: theme.spacing(10),
    left: theme.spacing(10),
  },
}));

const allLayers = [
  ...Object.keys(layout.objects).map((key) => ({
    name: key,
    color: layout.objects[key].color,
  })),
  ...Object.keys(layout.items).map((key) => ({
    name: key,
    color: layout.items[key].color,
  })),
];

export default function Simulation({
  children,
  settings = { showLayers: false },
}) {
  const classes = useStyles();
  const scale = useScrollZoom(0.4);
  const [selectedElement, setSelectedElement] = useState(null);
  const [showLayers, setShowLayers] = useState(settings.showLayers);
  const [layersToShow, setLayersToShow] = useState([
    ...Object.keys(layout.objects),
    ...Object.keys(layout.items),
  ]);

  useEffect(() => {
    setShowLayers(settings.showLayers);
  }, [settings.showLayers]);

  const selectElement = (element) => {
    setSelectedElement(element);
  };

  const clearElement = () => {
    setSelectedElement(null);
  };

  const closeLayers = () => {
    setShowLayers(false);
  };

  const layerToggle = (layer, value) => {
    if (value) {
      setLayersToShow([...layersToShow, layer]);
    } else {
      setLayersToShow(layersToShow.filter((v) => v !== layer));
    }
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
        {Object.entries(layout.objects)
          .filter(([name, conf]) => layersToShow.includes(name))
          .map(([name, objDef]) => (
            <Layer
              key={name}
              settings={{ name, elements: objDef.ids.length }}
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
        {Object.entries(layout.items)
          .filter(([name, conf]) => layersToShow.includes(name))
          .map(([name, objDef]) => (
            <Layer
              key={name}
              settings={{ name, elements: objDef.ids.length }}
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
      {showLayers && (
        <LayersList
          className={classes.layerList}
          layers={allLayers}
          layersShown={layersToShow}
          onSelect={layerToggle}
          onClose={closeLayers}
        />
      )}
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
