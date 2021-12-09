from models.safari import Safari
from models.animals import Lion, Zebra
from time import sleep
import random


if __name__ == '__main__':
    s = Safari(40, 20)
    s.visualise(println=True)
    niko = Lion(s, 'male', 'Nixon')
    qna = Lion(s, 'female', 'Julia')
    foxy = Lion(s, 'male', 'Pielat')
    s.insert(niko, (5, 10))
    s.insert(qna, (2, 5))
    s.insert(foxy, (2, 1))
    [s.insert(Zebra(s, random.choice(['female', 'male'])), (x, 19)) for x in range(25)]
    s.visualise(println=True)

    i = 0
    while True:
        s.make_random_moves()
        x = s.visualise(println=True, count_species=True)
        sleep(0.05)
        i += 1
