import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import ListSubheader from "@material-ui/core/ListSubheader";
import DashboardIcon from "@material-ui/icons/Dashboard";
import PeopleIcon from "@material-ui/icons/People";
import ListAltIcon from '@material-ui/icons/ListAlt';
import LayersIcon from "@material-ui/icons/Layers";
import AssignmentIcon from "@material-ui/icons/Assignment";

export const mainListItems = ({ selected = [], onClick = () => {} }) => (
  <div>
    <ListItem
      button
      onClick={() => onClick("dashboard")}
      selected={selected.includes("dashboard")}
    >
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
    <ListItem
      button
      onClick={() => onClick("agents")}
      selected={selected.includes("agents")}
    >
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary="Agents" />
    </ListItem>
    <ListItem
      button
      onClick={() => onClick("flights")}
      selected={selected.includes("flights")}
    >
      <ListItemIcon>
        <ListAltIcon />
      </ListItemIcon>
      <ListItemText primary="Flights" />
    </ListItem>
    <ListItem
      button
      onClick={() => onClick("layers")}
      selected={selected.includes("layers")}
    >
      <ListItemIcon>
        <LayersIcon />
      </ListItemIcon>
      <ListItemText primary="Layers" />
    </ListItem>
  </div>
);

export const secondaryListItems = () => (
  <div>
    <ListSubheader inset>Saved reports</ListSubheader>
    <ListItem button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Current run" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Last run" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="All runs" />
    </ListItem>
  </div>
);
