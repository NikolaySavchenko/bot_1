import os
import requests
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}', }
    payload = {}
    while True:
        try:
            response = requests.get(long_poling_url, headers=headers, params=payload, timeout=5)
            response.raise_for_status()
            if response.json()['new_attempts']:
                for attempt in response.json()['new_attempts']:
                    bot.send_message(text=f"Преподаватель проверил работу: {attempt['lesson_title']}",
                                     chat_id=tg_chat_id)
                    bot.send_message(text=f"Ссылка: {attempt['lesson_url']}",
                                     chat_id=tg_chat_id)
                    if attempt['is_negative']:
                        bot.send_message(text="К сожалению, в работе нашлись недочеты",
                                         chat_id=tg_chat_id)
                    else:
                        bot.send_message(text='Преподавателю все понравилось, можно приступать к следующему уроку',
                                         chat_id=tg_chat_id)
                payload = {'timestamp': response.json()['last_attempt_timestamp']}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
        except KeyError:
            continue
    return


if __name__ == '__main__':
    main()
