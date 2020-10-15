import organism
import pygame
import copy

ENERGY = 500
daynumber = 0


def start_day(predators, foods, screen_width, screen_height):
    global daynumber
    old_predators = copy.deepcopy(predators)
    predators.clear()

    sum = 0

    for predator in old_predators:
        sum += predator.speed
        if predator.food_eaten > 1:
            predator.breed(predators, 1)
        if predator.food_eaten > 0:
            predators.append(predator)
    daynumber += 1
    print("Average speed on day", daynumber, "was", (sum / len(old_predators)))

    for predator in predators:
        predator.food_eaten = 0
        predator.energy = ENERGY
        predator.randomize_position(screen_width, screen_height)

    for food in foods:
        food.eaten = False
        food.randomize_position(screen_width, screen_height)


def main():
    width = 400
    height = 400

    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode([width, height])
    running = True
    fps = 0

    foods = []
    predators = []

    for _ in range(5):
        predator = organism.Predator(0, 0, (255, 61, 194), 10, organism.random_range(1, 2), 50)

        predator.randomize_position(width, height)
        predators.append(predator)

    for _ in range(40):
        food = organism.Food(0, 0, 5)
        food.randomize_position(width, height)
        foods.append(food)

    clock = pygame.time.Clock()
    while running:
        screen.fill((255, 255, 255))

        day_over = True
        for predator in predators:
            speed_left = predator.speed
            predator.draw(screen)
            predator.energy -= predator.speed ** 2
            if predator.energy < 0:
                continue
            while speed_left > 0:
                if speed_left > 3:
                    speed_using = 3
                    speed_left -= 3
                else:
                    speed_using = speed_left
                    speed_left = 0
                predator.move(speed_using)
                predator.steer_randomly()
                closest = -1
                for food in (f for f in foods if not f.eaten):
                    if closest == -1 or food.distance_from(predator) < closest.distance_from(predator):
                        closest = food
                    if predator.collides_with(food):
                        food.eaten = True
                        predator.on_eat()

                if (not closest == -1) and closest.distance_from(predator) < (predator.sight + predator.radius):
                    predator.go_to_point(closest.x, closest.y)
            if predator.energy > 0:
                day_over = False

        for food in foods:
            if not food.eaten:
                food.draw(screen)

        if day_over:
            if not predators:
                running = False
            else:
                start_day(predators, foods, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()


        # Limit frames
        clock.tick(fps)


if __name__ == '__main__':
    main()
