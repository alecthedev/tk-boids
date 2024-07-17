from math import sqrt
from tkinter import Canvas


class Vector2:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, int):
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, int):
            return Vector2(self.x / other, self.y / other)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def normalize(self):
        if self == Vector2(0, 0):
            return Vector2(0, 0)
        return Vector2(self.x / self.magnitude(), self.y / self.magnitude())

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.x - self.y * other.y

    def distance_to(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


class Boid:
    def __init__(self, origin: Vector2, canvas: Canvas, tag: str) -> None:
        self.canvas = canvas
        self.tag = tag

        self.local_flock = []

        self.vertices = [
            Vector2(0, 0) + origin,
            Vector2(-5, 15) + origin,
            Vector2(0, 10) + origin,
            Vector2(5, 15) + origin,
        ]

        self.center = self.calc_center()
        self.velocity = Vector2(0, 0)
        self.sight_range = 100

    def update(self):
        self.draw()

    def calc_center(self):
        center = Vector2(0, 0)
        for i in range(len(self.vertices)):
            center.x = self.vertices[i].x / len(self.vertices)
            center.y = self.vertices[i].y / len(self.vertices)
        return center

    def draw(self):
        self.canvas.delete(self.tag)
        points = []
        for v in self.vertices:
            points.append(v.x)
            points.append(v.y)

        self.canvas.create_polygon(
            *points, fill="white", outline="white", tags=(self.tag)
        )


class BoidManager:
    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.boids = []

        self.canvas.bind("<Button-1>", self.spawn_boid)

    def update_boids(self):
        for b in self.boids:
            b.local_flock = self.manage_flock(b)
            b.update()
        self.canvas.after(10, self.update_boids)

    def manage_flock(self, target_boid) -> list[Boid]:
        # return list of boids within target boids sight
        flock = target_boid.local_flock
        for b in self.boids:
            if b is not target_boid:
                if target_boid.center.distance_to(b.center) <= target_boid.sight_range:
                    if b not in flock:
                        flock.append(b)
                        print(f"added {b.tag} to {target_boid.tag}'s local flock")
                elif b in flock:
                    flock.remove(b)
                    print(f"removed {b.tag} from {target_boid.tag}'s local flock")
        return flock

    def spawn_boid(self, event):
        new_boid = Boid(
            Vector2(event.x, event.y), self.canvas, f"boid_{len(self.boids)}"
        )
        self.boids.append(new_boid)
        print(f"{new_boid.tag} added")
