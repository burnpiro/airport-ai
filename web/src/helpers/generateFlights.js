import { defaultFlightConfig } from "./configs";

export default function generateFlights(
  flightData = [],
  config = defaultFlightConfig
) {
  const { color, border, borderWidth, fill } = config;

  return flightData.map((flight) => ({
    ...defaultFlightConfig,
    ...flight,
    date: new Date(flight.departure),
  }));
}
