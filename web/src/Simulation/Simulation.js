import { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import layout from "./layout.json";
import useScrollZoom from "../hooks/useScrollZoom";
import Layer from "./Layer/Layer";
import Planes from "./Layer/Planes";
import { defaultPointConfig, selectedPlaneConfig, PLANE_ITEMS_KEY } from "../helpers/configs";
import InfoBox from "./InfoBox/InfoBox";
import LayersList from "./LayersList/LayersList";
import { AgentLayer } from "./AgentLayer/AgentLayer";
import CastConnectedIcon from "@material-ui/icons/CastConnected";
import PortableWifiOffIcon from "@material-ui/icons/PortableWifiOff";
import {TimeTable} from "./TimeTable/TimeTable";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    height: "100%",
    overflow: "scroll",
    position: "relative",
  },
  layoutContainer: {
    position: "relative",
    maxWidth: "none",
  },
  layout: {
    backgroundColor: "#fff1b8",
    position: "absolute",
    top: 0,
  },
  items: {
    position: "absolute",
    top: 0,
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
  flightsList: {
    position: "fixed",
    top: theme.spacing(10),
    left: theme.spacing(10),
  },
  connectionStatusContainer: {
    position: "fixed",
    top: theme.spacing(9),
    right: theme.spacing(8),
    width: "30px",
    height: "30px",
  },
}));

const ConnectionStatus = ({ status }) => {
  const classes = useStyles();
  switch (status) {
    case "Open":
      return (
        <CastConnectedIcon
          aria-label={"Connected with the server :)"}
          style={{
            color: "green",
          }}
          className={classes.connectionStatusContainer}
        />
      );
    default:
      return (
        <PortableWifiOffIcon
          aria-label={"Cannot connect with the server :("}
          style={{
            color: "red",
          }}
          className={classes.connectionStatusContainer}
        />
      );
  }
};

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
  settings = { showLayers: false, showFlights: false },
}) {
  const classes = useStyles();
  const scale = useScrollZoom(0.1);
  const [selectedElement, setSelectedElement] = useState(null);
  const [showLayers, setShowLayers] = useState(settings.showLayers);
  const [connectionStatus, setConnectionStatus] = useState(settings.showLayers);
  const [gates, setGates] = useState([]);
  const [layersToShow, setLayersToShow] = useState([
    ...Object.keys(layout.objects),
    ...Object.keys(layout.items),
    'gates'
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

  const onStatusChange = (newStatus) => {
    setConnectionStatus(newStatus);
  };

  const onGatesChange = (newGates) => {
    if(Array.isArray(newGates) && newGates.length > 0 && (typeof newGates[0] !== "object" || newGates[0] == null)) {
      newGates = newGates.map((flightId, idx) => ({gateId: idx, flightId: flightId}))
    }
    setGates(newGates);
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

  return (
    <div className={classes.root} style={{}}>
      <div
        className={classes.layoutContainer}
        style={{
          transform: `scale(${Number(scale).toFixed(1)})`,
        }}
      >
        <div
          className={classes.layout}
          style={{
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
        </div>
        <div className={classes.items}>
          {Object.entries(layout.items)
            .filter(([name, conf]) => name !== PLANE_ITEMS_KEY)
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
        <div className={classes.items}>
          {[["gates", layout.gates]]
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
        <div className={classes.items}>
          {[[PLANE_ITEMS_KEY, layout.items[PLANE_ITEMS_KEY]]]
            .filter(([name, conf]) => layersToShow.includes(name))
            .map(([name, objDef]) => (
              <Planes
                key={name}
                settings={{ name, elements: objDef.ids.length }}
                points={objDef.points}
                ids={objDef.ids}
                onElementClick={selectElement}
                selectedPlanes={gates.filter(el => el.flightId != null).map(el => el.gateId)}
                flightNumbers={gates.filter(el => el.flightId != null)}
                config={{
                  ...defaultPointConfig,
                  color: objDef.color,
                  fill: objDef.fill
                }}
              />
            ))}
        </div>
        <div className={classes.items}>
          <AgentLayer onConnectionStatusChange={onStatusChange} />
        </div>
      </div>
      <ConnectionStatus status={connectionStatus} />
      {showLayers && (
        <LayersList
          className={classes.layerList}
          layers={allLayers}
          layersShown={layersToShow}
          onSelect={layerToggle}
          onClose={closeLayers}
        />
      )}
      {settings.showFlights && (
        <TimeTable
          className={classes.flightsList}
          onClose={closeLayers}
          onGatesChange={onGatesChange}
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
