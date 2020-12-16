import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  pointStyle: {
    position: "absolute",
    transition: "all 0.5s linear"
  },
}));

export default function Agent({ styles, position, size }) {
  const classes = useStyles();
  return (
    <svg
      className={classes.pointStyle}
      style={{ left: position.x, top: position.y }}
      height={size}
      width={size}
    >
      <circle cx={size/2} cy={size/2} r={size/2} style={styles} />
    </svg>
  );
}
