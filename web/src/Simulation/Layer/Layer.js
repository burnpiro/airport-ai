import { Fragment } from "react";
import { makeStyles } from "@material-ui/core/styles";
import generateBlocks from "../../helpers/generateBlocks";
import Block from "../Block/Block";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
  },
}));

export default function Layer({
  points,
  config,
  ids,
  settings,
  children,
  onElementClick,
}) {
  const classes = useStyles();

  const blocks = generateBlocks(points, config).map((block, id) => {
    return (
      <Block
        key={ids[id]}
        className={classes.pointStyle}
        points={block.points}
        position={block.position}
        styles={block.style}
        onClick={onElementClick}
        name={settings.name}
        message={`Elements in group: ${settings.elements}`}
      />
    );
  });
  return <Fragment>{blocks}</Fragment>;
}
