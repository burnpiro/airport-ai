const defaultPointConfig = {
  color: "#AAAAAA",
  border: "#666666",
  borderWidth: 2,
  fill: true,
};

const selectedPlaneConfig = {
  color: "#d62828",
  border: "#8A1919",
  stroke: "#d62828",
  fill: "#d62828",
  borderWidth: 2,
}

const defaultFlightConfig = {
  id: "",
  flightNum: "",
  from: "",
  dest: "",
  status: "On Time",
  departure: "2020-12-17T22:59:06+0000",
  gateNum: "1",
};

const PLANE_ITEMS_KEY = "planes";

export { defaultPointConfig, defaultFlightConfig, selectedPlaneConfig, PLANE_ITEMS_KEY };
