from dataclasses import dataclass
from dataclasses import field

@dataclass
class Restaurant:
    name: str
    placeID: str
    label: str
    address: str
    location: dict
    command: str
    GRating: float
    raitingTotal: float
    detailRating: list[int] = field(default_factory=list)


    def __init__(self, name: str, placeID: str = 0, label:str = "", address: str = "", location: dict = {}, command: str = "", GRating: float = 0,raitingTotal: int = 0, detailRating: list[int] = [0,0,0,0,0]):
        self.name = name
        self.placeID = placeID
        self.label = label
        self.address = address
        self.location = location
        self.command = command
        self.GRating = GRating
        self.raitingTotal = raitingTotal
        self.detailRating = detailRating

    def print(self):

        print(f"Name: {self.name}")
        print(f"label: {self.label}")
        print(f"placeID: {self.placeID}")
        print(f"address: {self.address}")
        print(f"location: {self.location}")
        print(f"rating: {self.GRating}")
        print(f"userRatingTotal: {self.raitingTotal}")
        print(f"detailRating: {self.detailRating}")
        print(f"command: {self.command}")
