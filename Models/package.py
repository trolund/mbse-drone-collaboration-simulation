from tokenize import String


class Package:

    weight: int
    width: int
    height: int
    address: String

    def __init__(self, wight, width, height, address):
        super().__init__()
        self.weight = wight
        self.width = width
        self.height = height
        self.address = address
 

