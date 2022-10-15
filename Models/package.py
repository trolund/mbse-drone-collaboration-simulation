import random

class Package:

    weight: int
    address: list

    def __init__(self, weight, address):
        super().__init__()
        self.weight = weight
        self.address = address
    def __str__(self): 
        return (f"Package of weight {self.weight} should be delivered to {self.address}")



