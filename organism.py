import pygame
import math
import random


def random_range(a, b):
    return a + random.random() * (b - a)


class Circle:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, circle):
        return (self.x - circle.x) ** 2 + (self.y - circle.y) ** 2 < (self.radius + circle.radius) ** 2

    def randomize_position(self, screen_width, screen_height):
        self.x = random_range(0, screen_width)
        self.y = random_range(0, screen_height)

    def distance_from(self, circle):
        return math.sqrt((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2)


class Predator(Circle):
    def __init__(self, x, y, color, radius, speed, sight=20):
        Circle.__init__(self, x, y, color, radius)
        self.energy = 500
        self.speed = speed
        self.food_eaten = 0
        self.velocity = (-1, 1)
        self.wandering = True
        self.sight = sight
    def move(self, moving):

        self.x += self.velocity[0]/self.speed * moving
        self.y += self.velocity[1]/self.speed * moving

    def get_angle(self):
        if self.velocity[1] < 0:
            return 2 * math.pi - math.acos(self.velocity[0] / math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2))
        else:
            return math.acos(self.velocity[0] / math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2))

    def adjust_angle(self, angle):
        new_angle = self.get_angle() + angle
        self.velocity = (self.speed * math.cos(new_angle), self.speed * math.sin(new_angle))

    def steer_randomly(self):
        if self.wandering:
            self.adjust_angle(random_range(-423, 423) / 1000)

    def go_to_point(self, x, y):
        length = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        self.velocity = (self.speed * (x - self.x) / length, self.speed * (y - self.y) / length)

    def on_eat(self):
        self.food_eaten += 1

    def breed(self, organisms, count):
        for _ in range(count):
            organisms.append(Predator(0, 0, self.color, self.radius, self.speed + random_range(-0.1, 0.1), self.sight))

    def draw(self, surface):
        # Draw fields of vision
        # pygame.draw.circle(surface, (162, 166, 171), (int(self.x), int(self.y)), self.radius + self.sight)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Food(Circle):
    def __init__(self, x, y, radius, color=(75, 199, 54)):
        Circle.__init__(self, x, y, color, radius)
        self.eaten = False
