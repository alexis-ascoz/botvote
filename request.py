import sys
import requests
import re
import time

exit = True


def getPoint(username, password):
    res = connect(username, password)
    return res.text.split(';')[1] if res else 0


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
            result.timeUntilVote = getTimeUntilVote(result.cookies)

            print('Connecté : ' + text[2] + ' - ' + text[1] + ' pts' +
                  (' - ' + time.strftime('%H:%M:%S', time.gmtime(result.timeUntilVote)) + ' cooldown' if result.timeUntilVote != 0 else ''))

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


def getTimeUntilVote(cookies):
    try:
        result = requests.post(
            'https://area-serveur.eu/voter.php', data={'step': 1}, cookies=cookies)

        text = result.text.split(';')

        return int(text[1]) if text[0] == '-1' else 0

    except Exception as ex:
        print('Erreur lors du vote : ')
        print(ex)


def vote(username, password, out):
    timeDelta = 30

    result = connect(username, password)

    if result != None:
        if (result.timeUntilVote):
            return result.timeUntilVote + timeDelta

        cookies = result.cookies

        url = 'https://area-serveur.eu/voter.php'

        data = {
            'step': 2,
            'out_value': out
        }

        try:
            result = None

            result = requests.post(url, data=data, cookies=cookies)

            if result.text == '1':
                print('Vote réussi pour ' + username)

                return 10800 + timeDelta
            else:
                print('Le vote à échoué pour ' + username +
                      " mais il semble qu'il soit tout de même possible de voter.")

        except Exception as ex:
            print('Erreur lors du vote : ')
            print(ex)
            
    if (exit):
        sys.exit(1)
    else:
        return timeDelta
