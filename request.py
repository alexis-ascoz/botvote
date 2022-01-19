import requests
import re
import time
from fp.fp import FreeProxy


def getPoint(username, password):
    return connect(username, password).text.split(';')[1]


def connect(username, password):
    url = 'https://area-serveur.eu/template/connexion.php'

    data = {
        'username': username,
        'password': password
    }

    try:
        result = requests.post(url, data=data)

        text = result.text.split(';')

        if text[0] == 'valid':
            print('Connecté : ' + text[2] + ' - ' + text[1] + ' pts')
            return result
        else:
            print('Mauvais mot de passe pour ' + username + '.')

    except Exception as ex:
        print('Erreur lors de la connexion : ')
        print(ex)


def getOutValue():
    url = 'https://www.rpg-paradize.com/site-NEW++Area-serveur.eu++1.36++Oriente+PvM+-114221'

    try:
        result = requests.get(url)

        regex = re.search("Clic Sortant : (.+)</div>", result.text)

        if regex:
            print('Valeur out : ' + regex.group(1))
            return regex.group(1)
        else:
            print("La valeur out n'a pas été trouvée.")

    except Exception as ex:
        print('Erreur lors de la recherche de la valeur out : ')
        print(ex)


def vote(username, password, out):
    timeDelta = 180

    result = connect(username, password)

    if result != None:
        cookies = result.cookies

        url = 'https://area-serveur.eu/voter.php'

        data = {
            'step': 2,
            'out_value': out
        }

        try:
            result = None
            while result == None:
                result = voteWithProxy(url, data, cookies)

            if result.text == '1':
                print('Vote réussi pour ' + username)
            else:
                result = requests.post(url, data={'step': 1}, cookies=cookies)

                text = result.text.split(';')

                if text[0] == '-1':
                    timeUntilVote = int(text[1])

                    print('Le vote sera possible dans ' +
                          time.strftime('%H:%M:%S', time.gmtime(timeUntilVote)) +
                          ' pour ' + username + '.')

                    return timeUntilVote + timeDelta
                else:
                    print('Le vote à échoué pour ' + username +
                          " mais il semble qu'il est tout de même possible de voter.")

        except Exception as ex:
            print('Erreur lors du vote : ')
            print(ex)

    return timeDelta


def voteWithProxy(url, data, cookies):
    try:
        proxy = FreeProxy(rand=True).get()

        proxies = {
            'https': proxy
        }

        return requests.post(url, data=data, cookies=cookies, proxies=proxies)

    except Exception as ex:
        print('Erreur lors du vote avec proxy : ')
        print(ex)

        return None
