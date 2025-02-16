import sys, pygame, random
from pygame.locals import *
from germ import Virus
from medic import Medic

# pygame variables
pygame.init()
clock = pygame.time.Clock()
size = (width, height) = (400, 300)
screen = pygame.display.set_mode(size)

# define sprite groups
germs = pygame.sprite.Group()
medics = pygame.sprite.Group()

# starting conditions
num_germs = 5
num_medics = 1
split_time = 500

# data collection variables
showDisplay = True
notDone = True

# data analysis functions
def process_data():
    pass

# game setup
def init_sprites():
    germs.empty()
    for g in range(num_germs):
        germs.add(Virus((random.randint(0, width), random.randint(0, height)), split_time))

    medics.empty()
    for m in range(num_medics):
        medics.add(Medic((random.randint(0, width), random.randint(0, height))))

def check_round():
    global num_medics, num_germs, split_time, notDone
    if len(germs) < 1:
        # medics "won"
        split_time -= 50
        if split_time > 10:
            init_sprites()
        else:
            notDone = False
    elif len(germs) > (num_germs * split_time) // 2:
        # viruses "won"
        num_medics += 1
        init_sprites()

def main():
    init_sprites()

    while notDone:
        if showDisplay:
            clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        # update sprites and game things
        germs.update(size, germs)
        medics.update(size)
        pygame.sprite.groupcollide(medics, germs, False, True)

        check_round()

        if showDisplay:
            # draw sprites
            screen.fill("black")
            germs.draw(screen)
            medics.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    main()