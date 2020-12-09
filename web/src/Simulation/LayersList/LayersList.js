import { Fragment } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: 345,
  },
}));

export default function LayersList({
  className,
  onSelect,
  layersShown = [],
  layers = [],
  onClose = () => {},
}) {
  const classes = useStyles();

  const handleChange = (event) => {
    onSelect(event.target.name, event.target.checked);
  };

  return (
    <Card className={classes.root + ` ${className}`}>
      <CardHeader
        action={
          <IconButton aria-label="settings" onClick={onClose}>
            <CloseIcon />
          </IconButton>
        }
        title="Available Layers"
      />
      <CardContent>
        {layers.map((layer) => (
          <Fragment key={`layer_${layer.name}`}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={layersShown.includes(layer.name)}
                  onChange={handleChange}
                  name={layer.name}
                  color="default"
                  style={{
                    color: layer.color,
                    "&$checked": {
                      color: layer.color,
                    },
                  }}
                />
              }
              label={layer.name}
            />
            <br />
          </Fragment>
        ))}
      </CardContent>
    </Card>
  );
}
