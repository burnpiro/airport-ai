import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import CloseIcon from '@material-ui/icons/Close';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: 345,
  },
}));

export default function InfoBox({title, message, position, color, className, onClose = () => {}}) {
  const classes = useStyles();

  return (
    <Card className={classes.root + ` ${className}`}>
      <CardHeader
        avatar={
          <FiberManualRecordIcon aria-label="recipe" style={{ fontSize: 50, color: color}} />
        }
        action={
          <IconButton aria-label="settings" onClick={onClose}>
            <CloseIcon />
          </IconButton>
        }
        title={title}
        subheader={`Position: x:${position['x']}px, y:${position['y']}px `}
      />
      <CardContent>
        <Typography variant="body2" color="textSecondary" component="p">
          {message}
        </Typography>
      </CardContent>
    </Card>
  );
}