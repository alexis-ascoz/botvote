import request
import time
import sys


def getPoints(usr, pwd):
    sum = 0

    for i in range(11):
        sum += int(request.getPoint(usr + str(i), pwd))

    print('Total : ' + str(sum))


def voteAll(usr, pwd):
    while True:
        out = request.getOutValue()

        for i in range(11):
            timeToSleep = request.vote(usr + str(i), pwd, out)

        time.sleep(timeToSleep)


def vote(usr, pwd):
    out = request.getOutValue()
    request.vote(usr, pwd, out)


if len(sys.argv) == 3:
    vote(sys.argv[1], sys.argv[2])
else:
    print("Arguments incorrects. 'python3 main.py [username] [password]'")
