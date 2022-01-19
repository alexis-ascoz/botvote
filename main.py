import request
import time
import sys
import math


def vote(usr, pwd, startIndex):
    out = request.getOutValue()

    index = str(math.floor(time.gmtime().tm_hour / 3) % 4 + int(startIndex))

    print('Vote with ' + index + ' at ' + time.ctime())

    timeToSleep = request.vote(usr + index, pwd, out)

    if timeToSleep < 60:
        print('Waiting ' + str(timeToSleep) + ' seconds.\n')

        time.sleep(timeToSleep)

        request.vote(usr + index, pwd, startIndex)


if len(sys.argv) == 4:
    vote(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print(
        "Arguments incorrects. 'python3 main.py [username] [password] [count]'")
