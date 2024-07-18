import math
from random import randint
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

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        if self == Vector2(0, 0):
            return Vector2(0, 0)
        return Vector2(self.x / self.magnitude(), self.y / self.magnitude())

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)


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

        self.angle = -90
        self.center = self.calc_center()
        self.velocity = Vector2(0, 0)
        self.sight_range = 150
        self.max_speed = 5
        self.min_distance = 50

        self.adjustments = {
            "alignment": 5,
            "cohesion": 0.1,
            "separation": 1,
            "randomness": 0.5,
        }

    def update(self):
        if self.velocity == Vector2(0, 0):
            self.initialize_velocity()
        if self.local_flock:
            self.velocity = self.calc_all_adjustments()
        self.move()
        self.draw()

    def calc_center(self):
        center = Vector2(0, 0)
        for i in range(len(self.vertices)):
            center.x += self.vertices[i].x / len(self.vertices)
            center.y += self.vertices[i].y / len(self.vertices)
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

    def rotate(self, angle):
        cos_val = math.cos(math.radians(angle))
        sin_val = math.sin(math.radians(angle))
        new_vertices = []
        for v in self.vertices:
            new_x = (
                (v.x - self.center.x) * cos_val - (v.y - self.center.y) * sin_val
            ) + self.center.x
            new_y = (
                (v.x - self.center.x) * sin_val + (v.y - self.center.y) * cos_val
            ) + self.center.y
            new_vertices.append(Vector2(new_x, new_y))
        self.vertices = new_vertices
        self.center = self.calc_center()

    def turn_towards(self, target_direction):
        # take given Vector and rotate boid to face it
        target_direction = target_direction.normalize()
        current_direction = Vector2(
            math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        ).normalize()
        dot_product = current_direction.dot(target_direction)
        dot_product = max(min(dot_product, 1.0), -1.0)
        angle = math.acos(dot_product)

        if current_direction.cross(target_direction) < 0:
            angle = -angle

        max_turn_angle = math.radians(5)
        if abs(angle) > max_turn_angle:
            angle = max_turn_angle if angle > 0 else -max_turn_angle

        self.rotate(math.degrees(angle))
        self.angle += math.degrees(angle)

    def move(self):
        # self.velocity += self.random_velocity().scale(self.adjustments["randomness"])

        for vertex in self.vertices:
            vertex.x += self.velocity.x
            vertex.y += self.velocity.y
        self.center = self.calc_center()
        self.turn_towards(self.velocity)

        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize().scale(self.max_speed)

    def initialize_velocity(self):
        while self.velocity == Vector2(0, 0):
            self.velocity = self.random_velocity()

    def random_velocity(self):
        return Vector2(randint(-2, 2), randint(-2, 2)).normalize()

    def calc_alignment(self):
        # adjust toward avg heading of local flock
        avg_x = sum(b.velocity.x for b in self.local_flock) / len(self.local_flock)
        avg_y = sum(b.velocity.y for b in self.local_flock) / len(self.local_flock)
        move_vector = Vector2(avg_x, avg_y)
        return move_vector.scale(self.adjustments["alignment"])

    def calc_cohesion(self):
        # move toward center mass of local flock
        avg_x = sum(b.center.x for b in self.local_flock) / len(self.local_flock)
        avg_y = sum(b.center.y for b in self.local_flock) / len(self.local_flock)
        move_vector = Vector2(avg_x, avg_y) - self.center
        return move_vector.scale(self.adjustments["cohesion"])

    def calc_separation(self):
        # avoid crowding local flock mates
        move_vector = Vector2(0, 0)
        for b in self.local_flock:
            distance = self.center - b.center
            if distance.magnitude() < self.min_distance:
                move_vector += distance / distance.magnitude()

        return move_vector.scale(self.adjustments["separation"])

    def calc_all_adjustments(self):
        alignment = self.calc_alignment()
        cohesion = self.calc_cohesion()
        separation = self.calc_separation()

        adjustment_vector = (alignment + cohesion + separation).normalize()

        if adjustment_vector.magnitude() < 0.5:
            adjustment_vector = adjustment_vector.normalize().scale(0.5)

        return adjustment_vector


class BoidManager:
    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.boids = []

        self.canvas.bind("<Button-1>", self.spawn_boid)

    def update_boids(self):
        for b in self.boids:
            b.local_flock = self.manage_flock(b)
            b.update()
        self.canvas.after(15, self.update_boids)

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
