import os
import requests
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=bot_token)
    updates = bot.get_updates()
    users_name = updates[0].message['chat']['first_name']
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}', }
    payload = {}
    while True:
        try:
            response = requests.get(long_poling_url, headers=headers, params=payload, timeout=60)
            response.raise_for_status()
            if response.json()['new_attempts']:
                for attempt in response.json()['new_attempts']:
                    bot.send_message(text=f"Преподаватель проверил работу: {attempt['lesson_title']}",
                                     chat_id=chat_id)
                    bot.send_message(text=f"Ссылка: {attempt['lesson_url']}",
                                     chat_id=chat_id)
                    if attempt['is_negative']:
                        bot.send_message(text="К сожалению, в работе нашлись недочеты",
                                         chat_id=chat_id)
                    else:
                        bot.send_message(text='Преподавателю все понравилось, можно приступать к следующему уроку',
                                         chat_id=chat_id)
                    payload = {'timestamp': attempt['timestamp']}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
    return


if __name__ == '__main__':
    main()
