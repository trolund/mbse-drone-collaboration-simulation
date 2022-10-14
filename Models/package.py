from tokenize import String


class Package:

    weight: int
    width: int
    height: int
    address: int

    def __init__(self, weight, width, height, address):
        super().__init__()
        self.weight = weight
        self.width = width
        self.height = height
        self.address = address
 

