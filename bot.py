# coding: utf-8
import requests
import datetime

token = '586566327:AAGyIOtqMRDLyDONnZrpyiV3n8aVZRtAhko'


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


greet_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def main():
    results = [
        u'Ты лучшая, все получилось =)))',
        u'Почему так жесток снег, оставляет твои следы',
        u'И по кругу зачем бег и бежишь от меня ты',
        u'Не даёт до утра спать, снег растаявший - он вода (3)',
        u'Ты одно лишь должна знать - я люблю тебя навсегда',
        u'Не даёт до утра спать, снег растаявший - он вода (5)',
        u'Ты одно лишь должна знать - я люблю тебя навсегда (6)',
        u'Почему голоса звёзд в полумраке едва слышны',
        u'Ветер слёзы дождя принёс, только слёзы мне не нужны',
        u'Разучилась смотреть вдаль, разучилась считать до ста (9)',
        u'Разучилась любить февраль, - он забрал тебя навсегда',
        u'Разучилась смотреть вдаль, разучилась считать до ста (11)',
        u'Разучилась любить февраль, - он забрал тебя навсегда (12)',
        u'Расстаются, когда ложь, засыпают, когда тьма',
        u'И по телу, когда дрожь - разрешают сводить с ума',
        u'Если хочешь идти - иди, если хочешь забыть - забудь',
    ]

    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
