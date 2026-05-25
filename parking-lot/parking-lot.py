from enum import Enum
import uuid
from datetime import datetime, timedelta
import math
from threading import Lock

class ParkingSpotStatus(Enum):
    EMPTY = "EMPTY"
    FULL = "FULL"
class ParkingSpotType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    LARGE_VEHICLE = "LARGE_VEHICLE"


# enum ParkingSpotStatus - "EMPTY" | "FULL"
# enum ParkingSpotType - "MOTORCYCLE" | "CAR" | "LARGE_VEHICLE"

# class ParkingSpot
# - status: ParkingSpotStatus
# - type: ParkingSpotType
# free_spot() -> ParkingSpotStatus
# occupy_spot() -> ParkingSpotStatus
# get_spot_type() -> ParkingSpotType
class ParkingSpot:
    def __init__(self, type: ParkingSpotType):
        self.type = type
        self.status = ParkingSpotStatus.EMPTY
    def set_status(self, status):
        self.status = status

# class Ticket
# - ticket_id: uuid
# - start_time: timestamp
# - end_time: timestamp
# - parking_spot: ParkingSpot
# - completed: bool
# complete_ticket() -> "SUCCESS" | "FAILURE"
class Ticket:
    def __init__(self, parking_spot: ParkingSpot, floor: int, start_time = datetime.now()):
        self.ticket_id = uuid.uuid4()
        self.start_time = start_time
        self.end_time = None
        self.parking_spot = parking_spot
        self.completed = False
        self.floor = floor
    def is_completed(self):
        return self.completed
    def get_parking_spot(self):
        return self.parking_spot


# class ParkingLot
# - parking_spots: ParkingSpot[]
# - hourly_rate: float
# - ticket_map: map<ticket_id, ticket>
# assign_parking_spot(ParkingSpotType) -> Spot
# free_parking_spot() -> Spot
# complete_ticket(ticket_id) -> float
# has_ticket_been_used() -> bool 
assign_spot_lock = Lock()
class ParkingLot:
    def __init__(self, parking_spots: dict[int, list[ParkingSpot]]):
        self.parking_spots = parking_spots
        self.ticket_map = {}
        self.max_penalty = 100
        self.parking_spot_hourly_rates = {ParkingSpotType.CAR: 5, ParkingSpotType.MOTORCYCLE: 3, ParkingSpotType.LARGE_VEHICLE: 8}
    def assign_parking_spot(self, type: ParkingSpotType, start_time=datetime.now()):
        with assign_spot_lock:
            spot = None
            spot_floor = None
            for floor, spots in self.parking_spots.items():
                matching_types = list(filter(lambda x: x.type == type, spots))
                spot = next((x for x in matching_types if x.status == ParkingSpotStatus.EMPTY), None)
                if spot is not None:
                    spot_floor = floor
                    break
            if spot is None:
                return None
            else:
                ticket = self.create_ticket(spot, spot_floor, start_time)
                self.ticket_map[ticket.ticket_id] = ticket
                spot.set_status(ParkingSpotStatus.FULL)
                return ticket.ticket_id
    def create_ticket(self, parking_spot: ParkingSpot, spot_floor: int, start_time = datetime.now()):
        ticket = Ticket(parking_spot, spot_floor, start_time)
        return ticket
    def list_spots(self):
        for spot in self.parking_spots:
            print(vars(spot))
    def list_tickets(self):
        for ticket in self.ticket_map.values():
            print(vars(ticket))
    def complete_ticket(self, ticket_id: uuid) -> float:
        ticket = self.ticket_map.get(ticket_id, None)
        if ticket is None:
            print("error, ticket not found")
            return 0
        if ticket.is_completed():
            print("error, ticket already used")
            return self.max_penalty
        total_cost = self.calculate_fee(ticket.start_time, datetime.now(), ticket.parking_spot.type)
        ticket.completed = True
        ticket.parking_spot.set_status(ParkingSpotStatus.EMPTY)
        return total_cost
    def calculate_fee(self, start_time, end_time, parking_spot_type):
        hourly_rate = self.parking_spot_hourly_rates[parking_spot_type]
        total_time = math.ceil((end_time - start_time).total_seconds() / 3600)
        print('total time: ', total_time)
        total_cost = total_time * hourly_rate
        return total_cost
        



spot1 = ParkingSpot(ParkingSpotType.CAR)
spot2 = ParkingSpot(ParkingSpotType.MOTORCYCLE)
spot3 = ParkingSpot(ParkingSpotType.LARGE_VEHICLE)
spot4 = ParkingSpot(ParkingSpotType.CAR)
spot5 = ParkingSpot(ParkingSpotType.MOTORCYCLE)
spot6 = ParkingSpot(ParkingSpotType.LARGE_VEHICLE)
spot7 = ParkingSpot(ParkingSpotType.CAR)
spot8 = ParkingSpot(ParkingSpotType.MOTORCYCLE)
spot9 = ParkingSpot(ParkingSpotType.LARGE_VEHICLE)

spots = {
    1: [spot1, spot2, spot3],
    2: [spot4, spot5, spot6],
    3: [spot7, spot8, spot9]
    }
parking_lot = ParkingLot(spots)
ticket1 = parking_lot.assign_parking_spot(ParkingSpotType.CAR, (datetime.now() - timedelta(hours=4)))
ticket2 = parking_lot.assign_parking_spot(ParkingSpotType.MOTORCYCLE)
print(ticket1)
# print(parking_lot.assign_parking_spot("TRUCK"))
# parking_lot.list_spots()
# parking_lot.list_tickets()
cost1 = parking_lot.complete_ticket(ticket1)
print('cost1: ', cost1)