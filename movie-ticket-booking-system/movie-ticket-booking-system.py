# design system that allows users to browse movies, select theaters and showtimes, book tickets, and manage reservations
import string
import uuid
from functools import reduce
from threading import Lock

seat_layout = []
for i in range(26):
    for j in range(20):
        letter = string.ascii_lowercase[i]
        seat_layout.append(letter + str(j+1))

# class MovieTicketBookingSystem
# - movies
# - theaters
reservation_lock = Lock()
class MovieTicketBookingSystem:
    def __init__(self, movies, theaters):
        self.movies = movies
        self.theaters = theaters
    def browse_movies(self):
        print('showing all movies: ', [movie.title for movie in self.movies])
    def get_showtime(self, theater, movie, time):
        showtimes = theater.showtimes
        showtime = next((x for x in showtimes if x.movie == movie and x.time == time), None)
        if showtime is None:
            print(f'no showings for {movie.title} available at {time}')
        else:
            return showtime
    def create_reservation(self, theater, movie, time, seat_ids, user):
        with reservation_lock:
            showtime = self.get_showtime(theater, movie, time)
            if showtime is None:
                print(f'no showings for {movie.title} available at {time}')
            else:
                reservation = showtime.create_reservation(seat_ids, user)
                if reservation is not None:
                    return reservation
                else:
                    print('error creating reservation')
    def list_reservations(self):
        showtimes = [theater.showtimes for theater in self.theaters]
        showtimes = [time for theater in showtimes for time in theater]
        reservations = []
        for showtime in showtimes:
            if len(showtime.reservations) == 0:
                continue
            res = showtime.reservations.values()
            for r in res:
                reservations.append(r)
        for reservation in reservations:
            print(f'reservation for {reservation.showtime.movie.title} at {reservation.showtime.time}')
    def cancel_reservation(self, reservation_id):
        showtimes = [theater.showtimes for theater in self.theaters]
        showtimes = [time for theater in showtimes for time in theater]
        found = False
        for showtime in showtimes:
            reservation = showtime.reservations.get(reservation_id, None)
            if reservation is not None:
                showtime.cancel_reservation(reservation_id)
                found = True
        if not found:
            print('reservation does not exist')
    

# Movie

# theater
# - screens
class Theater:
    def __init__(self):
        self.showtimes= []
    def add_showtime(self, showtime):
        self.showtimes.append(showtime)
    def list_showtimes(self):
        for showtime in self.showtimes:
            print(showtime.movie.title, " ", showtime.time)

# showtime
# - seats
# - movie
# - theater
class Showtime:
    def __init__(self, time, movie, theater, screen_id):
        self.time = time
        self.seats = seat_layout
        # self.seat_locks = [Lock() for seat in seat_layout]
        self.movie = movie
        self.theater = theater
        self.screen_id = screen_id
        self.reservations = {}
    def create_reservation(self, seat_ids, user):
        available_seats = self.list_available_seats()
        for seat_id in seat_ids:
            if seat_id not in self.seats:
                print('invalid seat id') 
                return
            if seat_id not in available_seats:
                print('seat is not available')
                return
        reservation = Reservation(seat_ids, self.screen_id, self, user)
        self.reservations[reservation.id] = reservation
        user.reservations.append(reservation)
        return reservation
    def list_reservations(self):
        for reservation in self.reservations.values():
            print(f'reservation for {self.movie.title} at {self.time}. Tickets: {[x for x in reservation.seat_ids]}')
    def cancel_reservation(self, reservation_id):
        reservation = self.reservations.get(reservation_id, None)
        if reservation is None:
            print(f'Reservation {reservation_id} does not exist or has been cancelled')
            return
        else:
            res = self.reservations.pop(reservation_id)
            if res is not None:
                print(f'reservation {res.id} succesfully deleted')
                index = res.user.reservations.index(res)
                del res.user.reservations[index]
    def list_available_seats(self):
        reservations = [x for x in self.reservations.values()]
        # print('reservations: ', reservations)
        taken_seats = [x.seat_ids for x in reservations]
        taken_seats = [seat for seats in taken_seats for seat in seats]
        available_seats = self.seats.copy()
        for seat in taken_seats:
            available_seats.remove(seat)
        # print('available seats: ', available_seats)
        return available_seats



# user
# - reservations
class User:
    def __init__(self):
        self.reservations = []

# reservation
# reservation can be for multiple tickets, but only a single showtime
# - tickets
class Reservation:
    def __init__(self, seat_ids, screen, showtime, user):
        self.id = uuid.uuid4()
        self.seat_ids = seat_ids 
        self.screen = screen
        self.showtime = showtime
        self.user = user

class Movie:
    def __init__(self, title):
        self.id = uuid.uuid4()
        self.title = title

movie1 = Movie('gone with the wind')
movie2 = Movie('goodfellas')
movie3 = Movie('casablanca')

movies = [movie1, movie2, movie3]
times = ['9:00', '11:00', '13:00']



def theater_builder(movies, times):
    theater = Theater()
    screens = []
    for i in range(len(movies)):
        screen = uuid.uuid4()
        screens.append([screen, movies[i]])
    for screen in screens:
        for time in times:
            # print('screen: ', screen)
            showtime = Showtime(time, screen[1], theater, screen[0])
            theater.add_showtime(showtime)
    return theater

theater1 = theater_builder(movies, times)
booking_system = MovieTicketBookingSystem(movies, [theater1])
# theater1.list_showtimes()
showtime = booking_system.get_showtime(theater1, movie1, '11:00')
user1 = User()
reservation1= booking_system.create_reservation(theater1, movie1, '11:00', ['a1', 'a2', 'a3'], user1)
showtime1 = theater1.showtimes[0]
reservation2 = booking_system.create_reservation(theater1, movie2, '11:00', ['b1', 'b2', 'b3'], user1)
reservation2 = booking_system.create_reservation(theater1, movie2, '11:00', ['b1', 'b2', 'b3'], user1)
reservation2 = booking_system.create_reservation(theater1, movie2, '11:00', ['b100', 'b2', 'b3'], user1)
booking_system.list_reservations()
booking_system.cancel_reservation(reservation1.id)
# showtime1.list_available_seats()

# def screen_builder(theater, )