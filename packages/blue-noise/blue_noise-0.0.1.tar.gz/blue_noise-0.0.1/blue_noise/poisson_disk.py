from collections import UserList
from math import ceil, cos, floor, pi, sin, sqrt
from random import randint, random
from typing import List, Tuple


class Grid(UserList):
    """
    A 2 dimensional grid represented as a list for storing valid sample points.
    Represents the background grid outlined in the Fast Poisson Disk Sampling algorithm
    """

    def __init__(self, src_width: int, src_height: int, radius: int) -> None:
        super().__init__()

        self.cellsize = radius / sqrt(2)
        self.radius = radius
        self.width = ceil(src_width / self.cellsize)
        self.height = ceil(src_height / self.cellsize)

        for _ in range(self.width * self.height):
            self.append(None)

    def coords(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """Returns the grid coordinates for a given sample point"""
        return floor(point[0] / self.cellsize), floor(point[1] / self.cellsize)

    @staticmethod
    def distance(point_1: Tuple[float, float], point_2: Tuple[float, float]) -> float:
        """Returns the euclidean distance between two points"""
        dx = point_1[0] - point_2[0]
        dy = point_1[1] - point_2[1]
        return sqrt(dx * dx + dy * dy)

    def fits(self, point: Tuple[float, float]) -> bool:
        """Scan the grid to check if a given point will fit. Only test nearby samples"""
        grid_x, grid_y = self.coords(point)
        yrange = range(max(grid_y - 2, 0), min(grid_y + 3, self.height))
        for point_x in range(max(grid_x - 2, 0), min(grid_x + 3, self.width)):
            for point_y in yrange:
                self.grid_point = self[point_x + point_y * self.width]
                if self.grid_point is None:
                    continue
                if self.distance(point, self.grid_point) <= self.radius:
                    return False
        return True


class FastPoissonDisk:
    """
    Implements a fast poisson disk sampling pattern in 2 dimensions
    as referenced here https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf
    """

    def __init__(self, width: int, height: int, radius: int, k_points: int = 300) -> None:
        self.width = width
        self.height = height
        self.radius = radius
        self.k_points = k_points

        self.grid = Grid(width, height, radius)
        point = width * random(), height * random()
        self.queue = [point]
        grid_x, grid_y = self.grid.coords(point)
        self.grid[grid_x + grid_y * self.grid.width] = point

    @staticmethod
    def random_disk(point: Tuple[float, float], radius: int) -> Tuple[float, float]:
        """Get a random point radially around the given point between the radius and 2 * radius"""
        alpha = 2 * pi * random()
        distance = radius * sqrt(3 * random() + 1)
        return (point[0] + distance * cos(alpha), point[1] + distance * sin(alpha))

    def samples(self) -> List[Tuple[int, int]]:
        while self.queue:
            q_index = randint(0, len(self.queue) - 1)
            q_point = self.queue[q_index]
            self.queue[q_index] = self.queue[-1]
            self.queue.pop()

            for _ in range(self.k_points):
                point = self.random_disk(q_point, self.radius)
                if not (0 <= point[0] < self.width and 0 <= point[1] < self.height) or not self.grid.fits(point):
                    continue

                self.queue.append(point)
                grid_x, grid_y = self.grid.coords(point)
                self.grid[grid_x + grid_y * self.grid.width] = point

        return [point for point in self.grid if point is not None]
