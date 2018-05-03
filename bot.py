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
            last_update = None
            # last_update = get_result[len(get_result)]

        return last_update


bot = BotHandler(token)
now = datetime.datetime.now()


def calc_rank(s):
    key = u'настя'
    d_key = {u'н': 1, u'а': 2, u'с': 3, u'т': 4, u'я': 5}
    d_res = {u'н': 0, u'а': 0, u'с': 0, u'т': 0, u'я': 0}
    for w in s.lower():
        if w in key:
            d_res[w] += 1

    res = 0
    for k, v in d_res.items():
        res += abs(v - d_key[k])

    return res


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

    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()

        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']

            rnk = min(calc_rank(last_chat_text), 15)

            bot.send_message(last_chat_id, results[rnk])

            new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
