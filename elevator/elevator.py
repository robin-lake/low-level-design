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
            self.select_elevator(request)
            self.requests.append(request)
        else:
            elevator.add_request(Request(floor, type), self.floors)
    def select_elevator(self, request):
        assigned = False
        for elevator in self.elevators:
            if elevator.get_current_floor() <= request.get_floor() and elevator.get_direction() == "UP" and request.get_request_type() == "PICKUP_UP":
                elevator.add_request(request)
                assigned = True
                break
            elif elevator.get_current_floor() >= request.get_floor() and elevator.get_direction() == "DOWN" and request.get_request_type() == "PICKUP_DOWN": 
                elevator.add_request(request)
                assigned = True
                break
            elif elevator.get_direction() == "IDLE":
                elevator.add_request(request)
                assigned = True
                break
        if assigned is False:
            self.elevators[0].add_request(request)

    def show_requests(self):
        print("** showing all requests")
        for request in self.requests:
            print(vars(request))
    def show_elevator_requests(self):
        print("** showing requests per elevator")
        for i, elevator in enumerate(self.elevators):
            print(f"elevator {i}: ")
            for request in elevator.requests:
                print(vars(request))
    def show_elevator_statuses(self):
        print("** showing elevator states")
        for i, elevator in enumerate(self.elevators):
            print(f"* elevator {i}: ")
            print(f"floor: {elevator.get_current_floor()}")
            print(f"direction: {elevator.get_direction()}")


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
        if len(self.requests) == 0:
            self.direction = "IDLE"
            return
        if self.direction == "UP" and self.floor + 1 <= max_floors:
            # print('going up')
            self.floor += 1
        elif self.direction == "DOWN" and self.floor > 1:
            # print('going down')
            self.floor -= 1
        elif self.direction == "IDLE" and len(self.requests) > 0:
            # print('starting elevator')
            self.start_elevator()
        self.complete_requests()
    def start_elevator(self):
        for request in self.requests:
            if request.floor > self.floor:
                self.direction = "UP"
                break
            elif request.floor < self.floor:
                self.direction = "DOWN"
                break

    def complete_requests(self):
        requests_to_complete = []
        for request in self.requests:
            if request.floor == self.floor:
                if request.get_request_type() == "PICKUP_UP" and self.direction == "UP":
                    requests_to_complete.append(request)
                elif request.get_request_type() == "PICKUP_DOWN" and self.direction == "DOWN":
                    requests_to_complete.append(request)
                elif request.get_request_type() == "DESTINATION":
                    requests_to_complete.append(request)
        for request in requests_to_complete:
            self.requests.remove(request)
    def add_request(self, request, max_floors):
        if request.get_floor() > max_floors or request.get_floor() < 1 or request.get_floor() == self.floor:
            return "invalid request"
        self.requests.append(request)
        if self.direction == "IDLE":
            if request.get_floor() > self.floor:
                self.direction = "UP"
            if request.get_floor() < self.floor:
                self.direction = "DOWN"

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
    def get_request_type(self):
        return self.request_type

elevator1 = Elevator()
elevator2 = Elevator()
elevator3 = Elevator()
orchestrator = Orchestrator([elevator1, elevator2, elevator3])
orchestrator.create_request(1, "PICKUP_UP", None)
orchestrator.step()
orchestrator.create_request(1, "PICKUP_UP", None)
orchestrator.step()
orchestrator.create_request(5, "DESTINATION", elevator1)
orchestrator.create_request(3, "PICKUP_UP", None)
orchestrator.step()
# orchestrator.show_requests()
# orchestrator.show_elevator_requests()
# orchestrator.show_elevator_statuses()
orchestrator.step()
# orchestrator.show_elevator_statuses()
orchestrator.step()
orchestrator.step()
orchestrator.step()
orchestrator.step()
orchestrator.step()
orchestrator.show_elevator_statuses()
orchestrator.create_request(2, "DESTINATION", elevator1)
orchestrator.show_elevator_statuses()
orchestrator.step()
orchestrator.step()
orchestrator.show_elevator_statuses()
orchestrator.step()
orchestrator.show_elevator_statuses()
orchestrator.show_elevator_requests()
orchestrator.step()
orchestrator.step()
orchestrator.show_elevator_statuses()
orchestrator.show_elevator_requests()