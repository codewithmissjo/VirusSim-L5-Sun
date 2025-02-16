import sys, pygame, random
from pygame.locals import *
import matplotlib.pyplot as plt
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
showDisplay = False
notDone = True
test_data = []
tests = 0
success = 0
case_samples = 10

# data analysis functions
def process_data():
    # [num_medics, num_germs, split_time, tests, success / tests * 100]
    x = []
    y = []
    for row in test_data:
        if row[-1] >= 75:
            # if the tests were successful
            x.append(row[2]) # split time
            y.append(row[0]) # num_medics
    fig = plt.figure()
    plt.scatter(x, y)
    plt.title("Doctors needed to prevent an outbreak\n started by 5 bacteria")
    plt.xlabel('split time (refreshes)')
    plt.ylabel('Doctors Needed')
    fig.savefig('data.png')

# game setup
def init_sprites():
    germs.empty()
    for g in range(num_germs):
        germs.add(Virus((random.randint(0, width), random.randint(0, height)), split_time))

    medics.empty()
    for m in range(num_medics):
        medics.add(Medic((random.randint(0, width), random.randint(0, height))))

def check_round():
    # checking if the current round is over, whether it was a success or failure
    global success 
    if len(germs) < 1:
        success += 1
        return True
    elif len(germs) > (num_germs * split_time) // 2:
        return True
    return False

def main():
    global num_germs, num_medics, tests, success, split_time, notDone
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

        if check_round():
            # the round is over
            tests += 1
            if tests >= case_samples:
                # we ran 10 tests with the same numbers!
                test_data.append([num_medics, num_germs, split_time, tests, success / tests * 100])
                print(test_data[-1])

                # details for the NEXT tests
                if test_data[-1][-1] == 0:
                    # BIG fail
                    num_medics += 2
                elif test_data[-1][-1] <= 75:
                    # MED fail
                    num_medics += 1
                else:
                    # Success for Drs, make the germs harder to destroy
                    split_time = round(split_time * 0.9)
                    if split_time < 10:
                        # no point in more tests, cause the split time is basically 0
                        notDone = False
                tests = 0
                success = 0
            # new round!
            init_sprites()

        if showDisplay:
            # draw sprites
            screen.fill("black")
            germs.draw(screen)
            medics.draw(screen)

            pygame.display.flip()
    process_data()

if __name__ == "__main__":
    main()