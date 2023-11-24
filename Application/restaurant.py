from dataclasses import dataclass
from dataclasses import field

@dataclass
class Restaurant:
    name: str
    placeID: str
    type: str
    address: str
    location: dict
    command: str
    GRating: float
    raitingTotal: float
    detailRating: list[float] = field(default_factory=list)
    review: str = ""


    def __init__(self, name: str, placeID: str = 0, type:str = "", address: str = "", location: dict = {}, command: str = "", GRating: float = 0,raitingTotal: int = 0, detailRating: list[float] = [0,0,0,0,0], review: str = ""):
        self.name = name
        self.placeID = placeID
        self.type = type
        self.address = address
        self.location = location
        self.command = command
        self.GRating = GRating
        self.raitingTotal = raitingTotal
        self.detailRating = detailRating
        self.review = review

    def print(self):

        print(f"Name: {self.name}")
        print(f"label: {self.type}")
        print(f"placeID: {self.placeID}")
        print(f"address: {self.address}")
        print(f"location: {self.location}")
        print(f"rating: {self.GRating}")
        print(f"userRatingTotal: {self.raitingTotal}")
        print(f"detailRating: {self.detailRating}")
        print(f"command: {self.command}")
