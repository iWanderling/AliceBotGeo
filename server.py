from tools import get_geo_coordinates, get_distance
from flask import Flask, request, jsonify
import logging


# Инициализация приложения и логирования:
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


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
    if req['session']['new']:
        res['response']['text'] = ('Добро пожаловать! Я - помощник, который может показать вам город, '
                                   'а также отправить вам расстояние между выбранными городами!')
        return

    # Получение городов:
    cities = get_cities(req)
    logging.info(cities)
    if not cities:
        res['response']['text'] = 'Вы не написали название города(-ов)!'

    elif len(cities) == 1:
        res['response']['text'] = ('Данный город находится в следующей стране: ' +
                                   get_geo_coordinates(cities[0], 'country'))

    elif len(cities) == 2:
        distance = get_distance(get_geo_coordinates(cities[0], 'coordinates'),
                                get_geo_coordinates(cities[1], 'coordinates'))
        res['response']['text'] = 'Расстояние между данными городами: ' + \
                                  str(round(distance)) + ' км.'
    else:
        res['response']['text'] = 'Вы отправили слишком много городов!'


def get_cities(req):
    cities = []

    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])

    return cities


if __name__ == '__main__':
    app.run()
