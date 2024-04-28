from tools import get_geo_coordinates, get_distance
from flask import Flask, request, jsonify
import logging


# Инициализация приложения и логирования:
app = Flask(__name__)

# Создаём словарь, где для каждого пользователя мы будем хранить его имя:
sessionStorage = {}


# Функция для отправки данных на сервер:
@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return jsonify(response)


# Обработчик диалога с пользователем:
def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Как вас зовут?'

        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    # Если пользователь не назвал своё имя - сообщаем об этом:
    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)

        if first_name is None:
            res['response']['text'] = 'Вы не назвали своё имя! Пожалуйста, скажите, как вас зовут?'

        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = (f'Добро пожаловать, {first_name.title()}! '
                                       f'Я - помощник, который может показать вам город, '
                                       'а также отправить вам расстояние между выбранными городами!')
            return
    else:
        # Получение городов:
        cities = get_cities(req)
        logging.info(cities)
        name = sessionStorage[user_id]['first_name'].capitalize()

        if not cities:
            res['response']['text'] = f'{name}, Вы не написали название города(-ов)!'

        elif len(cities) == 1:
            res['response']['text'] = (f'{name}, данный город находится в следующей стране: ' +
                                       get_geo_coordinates(cities[0], 'country'))

        elif len(cities) == 2:
            distance = get_distance(get_geo_coordinates(cities[0], 'coordinates'),
                                    get_geo_coordinates(cities[1], 'coordinates'))
            res['response']['text'] = f'{name}, расстояние между данными городами: ' + \
                                      str(round(distance)) + ' км.'
        else:
            res['response']['text'] = f'{name}, Вы отправили слишком много городов!'


def get_cities(req):
    cities = []

    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])

    return cities


def get_first_name(req):
    # Перебираем сущности:
    for entity in req['request']['nlu']['entities']:

        # Находим сущность с типом 'YANDEX.FIO':
        if entity['type'] == 'YANDEX.FIO':

            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None:
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
