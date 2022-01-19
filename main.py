from os import read
import request
import time

usr = ''
pwd = ''

def getPoints():
    sum = 0

    for i in range(11):
        sum += int(request.getPoint(usr + str(i), pwd))

    print('Total : ' + str(sum))


def vote():
    while True:
        out = request.getOutValue()

        #lineSplit = open("log", "r").readline().split(' ')

        for i in range(11):
            timeToSleep = request.vote(usr + str(i), pwd, out)

        time.sleep(timeToSleep)


getPoints()
