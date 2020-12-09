import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
  },
}));

export default function Agent({ points, styles, position }) {
  const classes = useStyles();
  return (
    <svg
      className={classes.pointStyle}
      style={{ left: position.minX, top: position.minY }}
      height={position.maxY - position.minY}
      width={position.maxX - position.minX}
    >
      <polygon points={points} style={styles} />
    </svg>
  );
}
