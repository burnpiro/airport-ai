import { defaultFlightConfig } from "./configs";

export default function generateFlights(
  flightData = [],
  config = defaultFlightConfig
) {
  return flightData.map((flight) => ({
    ...config,
    ...flight,
    date: new Date(flight.departure),
  }));
}
