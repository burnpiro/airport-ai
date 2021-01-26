import {useState} from "react";
import generateFlights from "../../helpers/generateFlights";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import { makeStyles } from "@material-ui/core/styles";
import useAPI from "../../hooks/useAPI";

const useStyles = makeStyles((theme) => ({
  root: {
    width: 700,
    maxWidth: 700,
  },
  title: {
    paddingLeft: theme.spacing(1),
    paddingTop: theme.spacing(1),
    textAlign: "center",
  },
  table: {
    maxHeight: "50vh",
  },
  body: {
    height: "100%",
    overflowY: "auto",
  },
}));

export const TimeTable = ({ className }) => {
  const classes = useStyles();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const { listOfObjects: listOfFlights } = useAPI("ws://localhost:8081", {
    mockDataURI: "/airport-ai/out.json",
  });

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const flights = generateFlights(listOfFlights.flights || []);
  return (
    <Paper className={classes.root + ` ${className}`}>
      <Typography
        component="h2"
        variant="h6"
        color="primary"
        gutterBottom
        className={classes.title}
      >
        Flights
      </Typography>
      <TableContainer className={classes.table}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Flight</TableCell>
              <TableCell>Route</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>Gate</TableCell>
              <TableCell align="right">Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {flights
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row) => (
                <TableRow key={row.id}>
                  <TableCell>{row.flightNum}</TableCell>
                  <TableCell>
                    {row.from} -> {row.dest}
                  </TableCell>
                  <TableCell>{row.date.toLocaleTimeString("de-DE")}</TableCell>
                  <TableCell>{row.gateNum}</TableCell>
                  <TableCell
                    align="right"
                    style={{
                      color: row.status === "On Time" ? "green" : "red",
                    }}
                  >
                    {row.status}
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      {flights.length !== 0 && (
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          count={flights.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onChangePage={handleChangePage}
          onChangeRowsPerPage={handleChangeRowsPerPage}
        />
      )}
      {flights.length === 0 && (
        <Typography
          component="h2"
          variant="h6"
          color="textSecondary"
          gutterBottom
          className={classes.title}
        >
          There are not active flights at the moment
        </Typography>
      )}
    </Paper>
  );
};
