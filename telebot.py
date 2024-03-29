import logging
import os
from time import sleep
import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger('database')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}', }
    payload = {}
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s %(lineno)d")
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    while True:
        try:
            response = requests.get(long_poling_url, headers=headers, params=payload, timeout=60)
            response.raise_for_status()
            review = response.json()
            if review['status'] == 'found':
                for attempt in review['new_attempts']:
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
                payload = {'timestamp': review['last_attempt_timestamp']}
            else:
                payload = {'timestamp': review['timestamp_to_request']}
        except requests.exceptions.ReadTimeout as err:
            continue
        except requests.exceptions.ConnectionError as err:
            sleep(30)
            continue
        except Exception as err:
            sleep(30)
            continue


if __name__ == '__main__':
    main()
