import requests
import os
from dotenv import load_dotenv


def main():
    url = 'https://dvmn.org/api/user_reviews/'
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    headers = {'Authorization': f'Token {dvmn_token}', }
    payload = {}
    while True:
        try:
            if payload == {}:
                response = requests.get(long_poling_url, headers=headers, timeout=5)
            else:
                response = requests.get(long_poling_url, headers=headers, params=payload, timeout=5)
            response.raise_for_status()
            if response.json()['new_attempts']:
                for attempt in response.json()['new_attempts']:
                    print(f"Преподаватель проверил работу: {attempt}")
            payload = {'timestamp': response.json()['new_attempts'][0]['timestamp']}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
    return


if __name__ == '__main__':
    main()
