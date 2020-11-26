# Object-Oriented Exercise from WQU datascience
# Exercise 1: Add and Subtract
from math import sqrt


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, others):
        return sqrt((self.x - others.x) ** 2 + (self.y - others.y) ** 2)

    def __repr__(self):
        return "point({},{})".format(self.x, self.y)

    def __add__(self, others):
        if isinstance(others, Point):
            return Point(self.x + others.x, self.y + others.y)
        else:
            raise TypeError("Expected values to be point but found {}".format(type(others)))

    def __sub__(self, others):
        if isinstance(others, Point):
            return Point(self.x - others.x, self.y - others.y)
        else:
            raise TypeError("Expected values to be point but found {}".format(type(others)))

    def __mul__(self, others):
        if isinstance(others, int):
            return Point(others * self.x, others * self.y)
        elif isinstance(others, Point):
            x_holder = self.x * others.x
            y_holder = self.y * others.y
            return x_holder + y_holder

    def __rmul__(self, others):
        return self.__mul__(others)


class Cluster(object):
    """FUNCTION FOR CLUSTERING CALCULATION"""

    def __init__(self, x, y):
        self.center = Point(x, y)
        self.points = []

    def update(self):
        temp = Point(0, 0)
        for point in self.points:
            temp.x += point.x
            temp.y += point.y
        self.center.x = temp.x / len(self.points)
        self.center.y = temp.y / len(self.points)
        self.points = []

    def add_point(self, point):
        return self.points.append(point)


def compute_result(points):
    """Method that runs the Algorithm"""
    points = [Point(*point) for point in points]
    a = Cluster(1, 0)
    b = Cluster(-1, 0)
    a_old = []
    for _ in range(10000):  # max iterations
        for point in points:
            if point.distance(a.center) < point.distance(b.center):
                # add the right point
                a.add_point(point)
            else:
                # add the right point
                b.add_point(point)
        if a_old == a.points:
            break
        a_old = a.points
        a.update()
        b.update()
    final = [(a.center.x, a.center.y), (b.center.x, b.center.y)]
    return sorted(final, reverse=True)
