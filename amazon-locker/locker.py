from datetime import datetime, timedelta
import secrets
import string
import threading

lock = threading.Lock()
# class Locker
# - compartments: Compartment[]
# - access tokens: map{token: Access Token}
# assign_compartment(size) -> {Compartment, Access Token} | "error"
# open_compartment(compartment, token) -> "success" | "error"
# release_expired_compartmente() -> "success" | "error"
class Locker:
    def __init__(self):
        self.compartments = []
        self.compartments.append(Compartment())
        self.access_tokens = {}
        
    def deposit_package(self, size):
        with lock:
            compartment = self.find_compartment(size)
            if compartment is None:
                return "error, no comparment available"
            token = compartment.generate_token()
            self.access_tokens[token.get_token()] = token
            compartment.set_status("Full")
            self.assigning_compartment = False
            return token.get_token()


    def find_compartment(self, size):
        empty = filter(lambda x: x.status == "Empty", self.compartments)
        compartment = next((x for x in empty if x.size == size), None)
        return compartment
    def pickup(self, token):
        access_token = self.access_tokens.get(token, None)
        if access_token is None:
            return "token not found"
        status = access_token.compartment.open(token)
        if status == "success":
            self.access_tokens.pop(token)
        return status




    
# class Compartment
# - status: "Full" | "Empty" | "Offline"
# - size: "Small" | "Medium" | "Large"
# - access token: Access Token | null
# open_compartment(access_token) -> "success" | "error"
class Compartment:
    def __init__(self, size):
        self.status = "Empty"
        self.access_token = None
        self.size = size
    def generate_token(self):
        self.access_token = AccessToken(self)
        return self.access_token
    def set_status(self, status):
        self.status = status
    def open(self, token):
        if self.access_token is None:
            return "no access token set"
        if token != self.access_token.get_token():
            return "wrong code"
        if self.status == "Empty" or self.staus == "Offline":
            return "cannot open compartment"
        else:
            if self.access_token.is_expired():
                return "token expired"
            self.status = "Empty"
            self.access_token = None
            return "success"

class AccessToken:
    def __init__(self, compartment, expiry):
        self.token = ''.join(secrets.choice(string.ascii_letters) for _ in range(12))
        self.expiry = expiry or datetime.now() + timedelta(weeks=1)
        self.compartment = compartment

    def get_token(self):
        return self.token
    def is_expired(self):
        return self.expiry < datetime.now()
# class Access Token
# - expiry: timestamp
# - token: strings
# - compartment: Compartment
# get_token() -> token
# check_expiry(token) -> bool