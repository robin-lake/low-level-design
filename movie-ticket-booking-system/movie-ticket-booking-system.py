# design system that allows users to browse movies, select theaters and showtimes, book tickets, and manage reservations
import string
import uuid

seat_layout = []
for i in range(26):
    for j in range(20):
        letter = string.ascii_lowercase[i]
        seat_layout.append(letter + str(j+1))

# class MovieTicketBookingSystem
# - movies
# - theaters
class MovieTicketBookingSystem:
    def __init__(self, movies, theaters):
        self.movies = movies
        self.theaters = theaters
    

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
        self.movie = movie
        self.theater = theater
        self.screen_id = screen_id
        self.reservations = {}
    def create_reservation(self, seat_ids, user):
        reservation = Reservation(seat_ids, self.screen_id, self, user)
        self.reservations[reservation.id] = reservation
    def list_reservations(self):
        for reservation in self.reservations.values():
            print(f'reservation for {self.movie.title} at {self.time}. Tickets: {[x for x in reservation.seat_ids]}')

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
theater1.list_showtimes()
user1 = User()
theater1.showtimes[0].create_reservation(['a1, a2, a3'], user1)
theater1.showtimes[0].list_reservations()

# def screen_builder(theater, )