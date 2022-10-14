import queue
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

def queue_package(amount_of_packages, possible_addresses, max_weight):
    min_weight = 200
    queue = []
    if amount_of_packages > len(possible_addresses):
        print("More packages than delivery spots!")
        return ("ERROR")

    for i in range(amount_of_packages):
        if min_weight == max_weight:
            weight = min_weight
        else:
            weight = random.randrange(min_weight,max_weight)
        point = random.randrange(0,len(possible_addresses))
        address = possible_addresses[point]
        del possible_addresses[point]
        package = Package(weight,address)
        queue.append(package)
    return queue


if __name__ == "__main__":
    possible_addresses = [[1,1],[2,2],[3,3],[4,4]]
    amount_of_packages = 3
    max_weight = 200
    queue = queue_package(amount_of_packages,possible_addresses,max_weight)
    for i in queue:
        print(i)



