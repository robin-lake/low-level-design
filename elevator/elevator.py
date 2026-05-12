from enum import Enum
import re
# enum Direction: "UP" | "DOWN"
# enum RequestType: "PICKUP_UP" | "PICKUP_DOWN" | "DESTINATION"
class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"
class RequestType(Enum):
    PICKUP_UP = "PICKUP_UP"
    PICKUP_DOWN = "PICKUP_DOWN"
    DESTINATION = "DESTINATION"

# class Orchestrator
# - elevators: Elevator[]
# - requests: Request[]
# handle_request(floor) - adds request to list, calls dispatch for elevator
# dispatch() - dispatches elevator
class Orchestrator:
    def __init__(self, elevators):
        self.elevators = elevators
        self.requests = []
        self.floors = 10
    def step(self):
        for elevator in self.elevators:
            elevator.step(self.floors)
    def create_request(self, floor, type, elevator):
        if elevator is None:
            request = Request(floor, type)
            self.assign_request_to_elevator(request)
            self.requests.append(request)
    def assign_request_to_elevator(self, request):
        for elevator in self.elevators:
            # check if:
            # elevator is higher than request and request is pickup down
            # elevator is lower than request and request is pickup up
            if elevator.get_current_floor() < request.get_floor() and elevator.get_direction == "UP" and request.get_request_type == "PICKUP_UP":
                elevator.add_request(request)
                break
            elif elevator.get_current_floor() > request.get_floor() and elevator.get_direction == "DOWN" and request.get_request_type == "PICKUP_DOWN": 
                elevator.add_request(request)
                break
            elif elevator.get_direction() == "IDLE":
                elevator.add_request(request)
                break
    def show_requests(self):
        print("showing all requests")
        for request in self.requests:
            print(vars(request))
    def show_elevator_requests(self):
        print("showing requests per elevator")
        for i, elevator in enumerate(self.elevators):
            print(f"elevator {i}: ")
            for request in elevator.requests:
                print(vars(request))


# class Elevator
# - floor: int
# - requests: Request[]
# - direction: "Up" | "Down" | "Stationary"
# add_request(request) - adds request to list
# get_current_floor - return self.floor
# get_direction - return self.direction
# step() - increment time, move up or down
class Elevator:
    def __init__(self):
        self.floor = 1
        self.requests = []
        self.direction = "IDLE"
    def get_current_floor(self):
        return self.floor
    def get_direction(self):
        return self.direction
    def step(self, max_floors):
        if self.direction == "UP" and self.floor + 1 <= max_floors:
            self.floor += 1
        elif self.direction == "DOWN" and self.floor > 1:
            self.floor -= 1
        requests_to_complete = []
        for request in self.requests:
            if request.floor == self.floor:
                requests_to_complete.append(request)
        for request in requests_to_complete:
            self.requests.remove(request)
    def add_request(self, request):
        self.requests.append(request)

# class Request
# - floor: int
# - direction: Direction
# - type: RequestType
# get_floor - return self.floor
# get_direction - return self.direction
# get_type -> RequestType
class Request:
    def __init__(self, floor, type):
        self.floor = floor
        self.request_type = type
    def get_floor(self):
        return self.floor
    def get_direction(self):
        return self.direction
    def get_request_type(self):
        return self.request_type

elevator1 = Elevator()
elevator2 = Elevator()
elevator3 = Elevator()
orchestrator = Orchestrator([elevator1, elevator2, elevator3])
orchestrator.create_request(1, "PICKUP_UP", None)
orchestrator.create_request(1, "PICKUP_UP", None)
orchestrator.create_request(3, "PICKUP_UP", None)
orchestrator.show_requests()
orchestrator.show_elevator_requests()