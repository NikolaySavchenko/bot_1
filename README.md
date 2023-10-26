# Notification Bot

It's connects to [DVMN](https://dvmn.org/) API's, check for verified works and notifies the user

## How to install


Python3 should already be installed. Use pip (or pip3, if there is a conflict with Python2) to install dependencies:

    pip install -r requirements.txt

For using you need your TOKEN from [DVMN](https://dvmn.org/api/docs/)

Also you need TOKEN for your [Bot in telegram](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

You should use environment variables. Create file name `.env` with next variables in the root directory.
In file `.env` only two line:

```
DVMN_TOKEN='here_is_your_own_TOKEN'
TG_BOT_TOKEN='here_is_your_own_TOKEN'
TG_CHAT_ID='here_is_your_own_chat_id'
```

Example for command line:
```
$ \bot_1> py telebot.py
```

### If you want to use Docker image:

The following assumes that you have installed Docker.
Example for command line:
```
$ docker pull  docker.io/homozx/bot1_docker # download the image

$ docker run --rm -e DVMN_TOKEN=here_is_your_own_TOKEN -e TG_BOT_TOKEN=here_is_your_own_TOKEN -e TG_CHAT_ID=here_is_your_own_chat_id -d bot1_docker
```
The Bot is working!