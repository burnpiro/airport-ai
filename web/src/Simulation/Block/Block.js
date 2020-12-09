import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
  },
  clickable: {
    cursor: "pointer"
  }
}));

export default function Block({ points, styles, position, onClick, name, message }) {
  const classes = useStyles();

  const selectElement = () => {
    onClick({
      position: {
        x: position.minX,
        y: position.minY
      },
      name: name,
      message,
      color: styles.color
    })
  }

  return (
    <svg
      className={classes.pointStyle + (onClick != null ? ` ${classes.clickable}` : '')}
      style={{ left: position.minX, top: position.minY }}
      height={position.maxY - position.minY}
      width={position.maxX - position.minX}
      onClick={selectElement}
    >
      <polygon points={points} style={styles} />
    </svg>
  );
}
