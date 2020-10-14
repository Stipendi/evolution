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

  #  pygame.init()
  #  pygame.display.init()
  #  screen = pygame.display.set_mode([width, height])
    running = True
    fps = 0

    foods = []
    predators = []

    for _ in range(5):
        predator = organism.Predator(0, 0, (255, 61, 194), 10, organism.random_range(0.1, 0.7))

        predator.randomize_position(width, height)
        predators.append(predator)

    for _ in range(30):
        food = organism.Food(0, 0, 5)
        food.randomize_position(width, height)
        foods.append(food)

    clock = pygame.time.Clock()
    while running:
       # screen.fill((255, 255, 255))

        day_over = True
        for predator in predators:
      #      predator.draw(screen)
            predator.move()
            if predator.energy > 0:
                day_over = False
            predator.steer_randomly()
            for food in foods:
                if (not food.eaten) and predator.collides_with(food):
                    food.eaten = True
                    predator.on_eat()

      #  for food in foods:
      #      if not food.eaten:
      #          food.draw(screen)

        if day_over:
            if not predators:
                running = False
            else:
                start_day(predators, foods, width, height)

  #      for event in pygame.event.get():
  #          if event.type == pygame.QUIT:
  #              running = False

  #      pygame.display.flip()


        # Limit frames
     #   clock.tick(fps)


if __name__ == '__main__':
    main()
