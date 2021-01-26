import random
from scipy.interpolate import interp1d


airports = [
    'Suceava', 'Reykjavik', 'Tel', 'Poznan', 'Tirana', 'Frankfurt', 'Cluj-Napoca', 'Debrecen', 'Wroclaw', 'Milan', 'Iasi', 'Sofia', 'Dublin', 'Belfast', 'Tenerife', 'Faro', 'Bacau', 'Krakow', 'Kaunas', 'Budapest', 'Constanta', 'Marrakesh', 'Lublin', 'Kiev', 'Timisoara', 'Vilnius', 'Lisbon', 'Katowice', 'Poprad', 'Gdansk', 'Malaga', 'Warsaw', 'Luqa', 'Palma', 'Istanbul', 'Bucharest', 'Olsztyn', 'St.', 'Larnaca',
    'Craiova', 'Vienna', 'Athens', 'Moscow', 'Chisinau', 'Thessaloniki', 'Targu', 'Bratislava', 'Belgrade', 'Riga', 'Varna', 'Kosice'
]


class Flights:
    def __init__(self, length, gate_ids):
        # self.flights_per_day = 1000
        self.flights_per_day = 100
        number_of_flights = int(self.flights_per_day * length)

        length = length*24*60

        self.flights = {}
        self.arrivals = []
        self.departures = []

        self.soon_departures = {}
        self.current_arrivals = {}
        self.gates = {gate_id: None for gate_id in gate_ids}
        self.gate_ids = gate_ids

        for i in range(number_of_flights):
            self.flights[i] = {
                "id": i,
                "scheduled": random.uniform(45, length),
                "from": random.choice(airports),
                "to": "Luton",
                "delay": 0,
                "gate": random.choice(gate_ids),
                "size": random.randrange(30, 70)
            }
            self.arrivals.append(i)

        for i in range(number_of_flights):
            id = i + number_of_flights
            self.flights[id] = {
                "id": id,
                "scheduled": random.uniform(45, length),
                "from": "Luton",
                "to": random.choice(airports),
                "from": "Luton",
                "delay": 0,
                "gate": random.choice(gate_ids),
                # "size": random.randrange(50, 180)
                "size": random.randrange(30, 70)
            }
            self.departures.append(id)

    def board_passenger(self, plane_id):
        self.soon_departures[plane_id]['passengers_on_board'] += 1

    def update(self, time, time_step):
        arrivals = list(
            filter(
                lambda x: self.flights[x]["scheduled"] +
                self.flights[x]["delay"] <= time, self.arrivals
            )
        )

        soon_departures = list(
            filter(
                lambda x: self.flights[x]["scheduled"] < time +
                45, self.departures
            )
        )

        for departure in soon_departures:
            if departure not in self.soon_departures:
                flight = self.flights[departure]
                t = flight["scheduled"]
                # passengers appear at airport between 45 and 5 minutes before scheduled departure
                agent_time = interp1d([0, 1], [t-60, t-20])

                self.soon_departures[departure] = {
                    "agent_arrivals": [
                        agent_time(random.betavariate(2, 2))
                        for _ in range(flight['size'])
                    ],
                    'flight_id': departure,
                    'departure_time': None,
                    'passengers_on_board': 0
                }

        for arrival in arrivals:
            if arrival not in self.current_arrivals:
                flight = self.flights[arrival]
                if self.gates[flight['gate']] is not None:
                    # assigned gate is not free
                    flight["delay"] += time_step
                    continue
                # arrival time
                t = flight["scheduled"] + flight["delay"]
                self.current_arrivals[arrival] = {
                    "agent_arrivals": [
                        random.uniform(t+5, t+20)
                        for _ in range(flight['size'])
                    ],
                    'flight_id': arrival,
                    'arrival_time': t
                }
                # assign flight to gate
                self.gates[flight['gate']] = arrival

        # Free gates after arrival is resolved
        to_remove = []
        for id, arrival in self.current_arrivals.items():
            flight = self.flights[id]
            if arrival['arrival_time'] + 25<time:
                # free gate and remove flight
                self.gates[flight['gate']] = None                
                to_remove.append(id)
                del self.flights[id]
                self.arrivals.remove(id)

        for id in to_remove:
            del self.current_arrivals[id]

        # put departing flights to gate        
        for id, arrival in self.soon_departures.items():
            flight = self.flights[id]
            departure_time = flight['scheduled'] + flight['delay']
            if departure_time - 30<time: # put airplane in gate 30 minutes before departure
                if self.gates[flight['gate']] is not None:
                    # if gate is not free - delay
                    flight['delay'] += time_step
                    continue

                self.gates[flight['gate']] = id
                arrival['departure_time'] = departure_time

        # depart flights
        to_remove = []
        for id, arrival in self.soon_departures.items():
            flight = self.flights[id]
            departure_time = flight['scheduled'] + flight['delay']
            if departure_time<time:
                if arrival['passengers_on_board'] < arrival['size']:
                    # not all passangers boarded - delay
                    flight['delay'] += time_step
                    continue

                to_remove.append()
                del self.flights[id]
                self.departures.remove(id)

        for id in to_remove:
            del self.soon_departures[id]
                

        # TODO: update delays

        agents_to_spawn = []
        # Spawn departing actors 
        
        for id, departure in self.soon_departures.items():
            to_remove = []
            for t in departure["agent_arrivals"]:
                if t < time:
                    agents_to_spawn.append({'position':'entrance', 'destination': id})
                    to_remove.append(t)

            for t in to_remove:
                departure["agent_arrivals"].remove(t)

        # Spawn arriving actors 
        
        for id, arrival in self.current_arrivals.items():
            to_remove = []
            flight = self.flights[id]
            for t in arrival["agent_arrivals"]:
                if t < time:
                    agents_to_spawn.append({'position': flight['gate'], 'destination': 'exit'})
                    to_remove.append(t)
        
            for t in to_remove:
                arrival["agent_arrivals"].remove(t)

        return agents_to_spawn

    def get_gate_of_flight(self, flight_id):
        return self.flights[id]['gate']