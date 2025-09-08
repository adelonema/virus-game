import random
import numpy as np
import math
from matplotlib import pyplot as plt
from collections import Counter


# =============================================================================
# Global variables:
# =============================================================================

TIMEFRAMES = 10
NUM_POINTS = 600
DIMENSIONS = 400
INF_DISTANCE = 20
INF_PROB = .1
RECOVERY_TIME = 20
RECOVERY_RESET = 30
SPEED = 7

STATUS2COLOR = {
    "Sane": "slategrey",
    "Infected": "indianred",
    "Recovered": "darkseagreen"
}

# =============================================================================
# Initialise class:
# =============================================================================

class Point:
    def __init__(self, x_start, y_start, dx, dy, status, recovery):
        self.x = x_start
        self.y = y_start
        self.dx = dx
        self.dy = dy
        self.status = status
        self.recovery = recovery

    # def info_str(self):
    #     return "Hallo ich bin ein Punkt.. x: " + str(self.x)

    def __str__(self):
        return (f"Point: x = {self.x}, y = {self.y}, dx = {self.dx}, "
                f"dy = {self.dy}, status = {self.status}, recovery = {self.recovery}")

    def __repr__(self):
        return self.__str__()
    
    def move(self):
        # Directional movement:
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # Check if selfs are out of bound and let them bounce off the wall:
        if self.x > DIMENSIONS:
            self.x = DIMENSIONS - (self.x - DIMENSIONS)
            self.dx = - self.dx
        elif self.x < 0:
            self.x = - self.x
            self.dx = - self.dx

        # Same for y coordinates:
        if self.y > DIMENSIONS:
            self.y = DIMENSIONS - (self.y - DIMENSIONS)
            self.dy = - self.dy
        elif self.y < 0:
            self.y = - self.y
            self.dy = - self.dy

        

# =============================================================================
# Create class instance:
# =============================================================================

all_points = [Point(np.random.randint(DIMENSIONS), np.random.randint(DIMENSIONS), (0.5 - np.random.random())
                    * SPEED, (0.5 - np.random.random()) * SPEED, "Sane", 0) for i in range(NUM_POINTS)]


# all_points = [Point(np.random.randint(DIMENSIONS), np.random.randint(DIMENSIONS), np.random.randint(360), (0.5 - np.random.random()) * SPEED, "Sane", 0) for i in range(NUM_POINTS)]

# plt.plot([point.x for point in all_points], [point.y for point in all_points], "o")
# plt.show()


# for point in all_points:

#     plt.plot(point.x, point.y, "o", color = STATUS2COLOR[point.status])

# plt.show()


# =============================================================================
# Set random point to be infected:
# =============================================================================

all_points[np.random.randint(NUM_POINTS)].status = "Infected"


# =============================================================================
# Initialise lists for number of sane, infected and recovered points
# =============================================================================

sanecum = []
infcum = []
recovcum = []

# =============================================================================
# Time frames: 
# 
#   Calculate the following per time frame
#       * Who gets infected
#       * The number of new infections and recoveries
#
#   Plot all updated points per time frame
#
#   Calculate the statistics and plot them per time frame
# 
# =============================================================================

for i in range(TIMEFRAMES):
    # Initialise lists for infected points
    infected_x = []
    infected_y = []

    # Within each time frame go through all points:
    for point in all_points:

        # Completely random movement:
        # point.x = point.x + (np.random.random() - .5) * 3
        # point.y = point.y + (np.random.random() - .5) * 3

        point.move()

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
                point.status = "Sane"
                point.recovery = 0

    # Write lists of infected coordinates into arrays
    infvec_x = np.array(infected_x)
    infvec_y = np.array(infected_y)

    # Koordinaten abrufen und checken, ob sie mit den Koordinaten von Punkten in der Infizierten-Liste liegen
    for point in all_points:
        dist = np.sqrt(np.abs(infvec_x - point.x) ** 2 +
                       np.abs(infvec_y - point.y) ** 2)
        if any(dist < INF_DISTANCE) and point.status == "Sane":
            if np.random.random() < INF_PROB:
                point.status = "Infected"

    plt.plot(all_points[1].x, all_points[1].y, "o",
             color=STATUS2COLOR[all_points[1].status])
    ax = plt.gca()
    ax.set_xlim([0, DIMENSIONS])
    ax.set_ylim([0, DIMENSIONS])
    plt.gca().set_aspect('equal')

    # Plot each time frame
    for point in all_points:
        plt.plot(point.x, point.y, "o", color=STATUS2COLOR[point.status])
    # plt.show()
    plt.savefig("./points/all_points" + str(i) + ".png")
    plt.close()

    # Calculate the number of infected points per timestep:

    infpertime = [j.status for j in all_points]
    cnt = Counter(infpertime)
    # sanecount = sanecum.count("Sane")
    sanecum.append(cnt["Sane"])
    infcum.append(cnt["Infected"])
    recovcum.append(cnt["Recovered"])

    # Plot them:

    plt.plot(sanecum, color=STATUS2COLOR['Sane'], label='Sane')
    plt.plot(infcum, color=STATUS2COLOR['Infected'], label='Infected')
    plt.plot(recovcum, color=STATUS2COLOR['Recovered'], label='Recovered')
    plt.xlabel("Time steps")
    plt.ylabel("Affected points")
    plt.legend(loc='center left')
    # plt.title('multiple plots')
    # plt.show()
    plt.savefig("./stats/cumplots" + str(i) + ".png")
    plt.close()
