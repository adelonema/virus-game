import random
import numpy as np
from matplotlib import pyplot as plt

# Globale Variablen:

NUM_POINTS = 400
DIMENSIONS = 200
INF_DISTANCE = 9
INF_PROB = .7
RECOVERY_TIME = 30
RECOVERY_RESET = 50


class Point:
    def __init__(self, x_start, y_start, status, recovery):
        self.x = x_start
        self.y = y_start
        self.status = status
        self.recovery = recovery

    def info_str(self):
        return "Hallo ich bin ein Punkt.. x: " + str(self.x)

    def __str__(self):
        return f"Point: x = {self.x}, y = {self.y}, status = {self.status}, recovery = {self.recovery}"

    def __repr__(self):
        return self.__str__()

# all_points = []
# for i in range(100):
#     all_points.append(Point(np.random.randint(100), np.random.randint(100)))

all_points = [Point(np.random.randint(DIMENSIONS), np.random.randint(DIMENSIONS), "Sane", 0) for i in range(NUM_POINTS)]

# plt.plot([point.x for point in all_points], [point.y for point in all_points], "o")
# plt.show()

color = {
    "Sane" : "lightseagreen",
    "Infected" : "orangered",
    "Recovered" : "deepskyblue"
}

# for point in all_points:
#
#     plt.plot(point.x, point.y, "o", color = color[point.status])
#
# plt.show()


# Set random point to be infected:
all_points[np.random.randint(NUM_POINTS)].status = "Infected"

# Time frames
for i in range(200):
    # Initialise lists for infected points
    infected_x = []
    infected_y = []

    # Within each time frame go through all points:
    for point in all_points:
        point.x = point.x + (np.random.random() - .5) * 3
        point.y = point.y + (np.random.random() - .5) * 3
        if point.status == "Infected":
            # Fill lists with coordinates of infected points
            infected_x.append(point.x)
            infected_y.append(point.y)
            # Increase recovery counter by 1 if infected
            point.recovery = point.recovery + 1
            if point.recovery > RECOVERY_TIME:
                point.status = "Recovered"
        if point.status == "Recovered":
            point.recovery = point.recovery + 1
            if point.recovery > RECOVERY_RESET:
                point.recovery = 0

    # Write lists of infected coordinates into arrays
    infvec_x = np.array(infected_x)
    infvec_y = np.array(infected_y)


    # Koordinaten abrufen und checken, ob sie mit den Koordinaten von Punkten in der Infizierten-Liste liegen
    for point in all_points:
        dist = np.sqrt(np.abs(infvec_x - point.x) ** 2 + np.abs(infvec_y - point.y) ** 2)
        if any(dist < INF_DISTANCE) and point.recovery == 0:
            if np.random.random() < INF_PROB:
                point.status = "Infected"


    # Plot each time frame
    for point in all_points:
        plt.plot(point.x, point.y, "o", color=color[point.status])

    #plt.show()
    plt.savefig("all_points" + str(i) + ".png")
    plt.close()


