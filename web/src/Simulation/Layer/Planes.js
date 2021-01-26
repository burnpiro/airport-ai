import { Fragment } from "react";
import { makeStyles } from "@material-ui/core/styles";
import generateBlocks from "../../helpers/generateBlocks";
import Block from "../Block/Block";
import { selectedPlaneConfig } from "../../helpers/configs";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
  },
  planeInfo: {
    textAlign: "center",
  },
}));

export default function Planes({
  points,
  config,
  ids,
  settings,
  children,
  onElementClick,
  selectedPlanes = [],
  flightNumbers = [],
}) {
  const classes = useStyles();

  const blocks = generateBlocks(points, config).map((block, id) => {
    // console.log(points)
    const flightNumber = selectedPlanes.includes(`${ids[id]}`)
      ? flightNumbers.find((el) => el.gateId === `${ids[id]}`)
      : null;
    return (
      <Block
        key={ids[id]}
        testId={`plane-${ids[id]}`}
        className={classes.pointStyle}
        points={block.points}
        position={block.position}
        styles={{
          ...block.style,
          ...(selectedPlanes.includes(`${ids[id]}`) ? selectedPlaneConfig : {}),
        }}
        onClick={onElementClick}
        name={settings.name}
        text={
          <span className={classes.planeInfo}>
            {flightNumber ? flightNumber.flightId : ""}
            <br />
            {flightNumber ? `G:${flightNumber.gateId}` : ""}
          </span>
        }
        message={`Num of planes: ${settings.elements}`}
      />
    );
  });
  return <Fragment>{blocks}</Fragment>;
}
