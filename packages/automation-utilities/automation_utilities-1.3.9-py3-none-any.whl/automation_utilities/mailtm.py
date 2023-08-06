import time
from requests import JSONDecodeError
import requests
import random
from automation_utilities import Generator, Exceptions


def domains():
    return [element['domain'] for element in requests.get('https://api.mail.tm/domains').json()['hydra:member']]


class Account:

    def __init__(self,
                 address: str = Generator.generate_email(random.choice(domains())),
                 password: str = Generator.generate_password()):
        self.address = address
        self.password = password
        data = {
            'address': address.lower(),
            'password': password
        }
        while True:
            try:
                self.id = requests.post('https://api.mail.tm/accounts', json=data).json()['id']
                break
            except KeyError:
                raise Exceptions.AccountError()
            except JSONDecodeError:
                pass
        while True:
            try:
                token = requests.post('https://api.mail.tm/token', json=data).json()['token']
                break
            except JSONDecodeError:
                pass
        self.headers = {'Authorization': f"Bearer {token}"}

    def messages(self):
        while True:
            while True:
                try:
                    resoponse = requests.get('https://api.mail.tm/messages', headers=self.headers).json()
                    break
                except JSONDecodeError:
                    pass
            if resoponse['hydra:totalItems'] > 0:
                messages = []
                for member in resoponse['hydra:member']:
                    url = f'https://api.mail.tm/messages/{member["id"]}'
                    while True:
                        try:
                            messages.append(requests.get(url, headers=self.headers).json()['html'])
                            break
                        except JSONDecodeError:
                            pass
                if resoponse['hydra:totalItems'] == 1:
                    return messages[0][0]
                else:
                    return messages[0]
            time.sleep(1)
