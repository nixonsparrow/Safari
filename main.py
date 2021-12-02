from models import Safari, Lion
from time import sleep


if __name__ == '__main__':
    s = Safari(20, 40)
    s.visualise(println=True)
    niko = Lion(s, 'male', 'Nikoś')
    qna = Lion(s, 'female', 'Julia')
    foxy = Lion(s, 'male', 'Lisunio')
    s.insert(niko, (5, 10))
    s.insert(qna, (2, 5))
    s.insert(foxy, (36, 19))
    s.visualise(println=True)

    while True:
        s.make_random_moves()
        s.visualise(println=True)
        sleep(0.05)
