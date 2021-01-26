import { Fragment } from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
  },
  textStyle: {
    position: "absolute",
    fontSize: "10vh",
    backgroundColor: "whitesmoke",
    borderRadius: "20%",
    borderColor: "black",
    borderWidth: "1vh",
    borderStyle: "dashed",
    transform: "translateX(-50%)"
  },
  clickable: {
    cursor: "pointer",
  },
}));

export default function Block({
  points,
  testId,
  styles,
  position,
  onClick,
  name,
  text,
  message,
}) {
  const classes = useStyles();

  const selectElement = () => {
    onClick({
      position: {
        x: position.minX,
        y: position.minY,
      },
      name: name,
      message,
      color: styles.color,
    });
  };

  return (
    <Fragment>
      <svg
        className={
          classes.pointStyle + (onClick != null ? ` ${classes.clickable}` : "")
        }
        style={{ left: position.minX, top: position.minY }}
        test-id={testId}
        height={position.maxY - position.minY}
        width={position.maxX - position.minX}
        onClick={selectElement}
      >
        <polygon points={points} style={styles} />
      </svg>
      {text != null && <span
        className={
          classes.textStyle
        }
        style={{ left: position.minX + 0.5*(position.maxX - position.minX), top: position.minY + 0.25*(position.maxY - position.minY) }}>{text.flightId}</span>}
    </Fragment>
  );
}
