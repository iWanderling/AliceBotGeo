import requests
import math


def get_distance(p1, p2):
    # p1 и p2 - это кортежи из двух элементов - координаты точек
    radius = 6373.0

    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

    distance = radius * c
    return distance


def get_geo_coordinates(city_name, type_info):
    # Получаем страну города:
    if type_info == 'country':
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                'geocode': city_name,
                'format': 'json'
            }
            data = requests.get(url, params).json()
            # все отличие тут, мы получаем имя страны
            return data['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        except Exception as e:
            status_error = e
            return

    # Получаем координаты города:
    elif type_info == 'coordinates':
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                'geocode': city_name,
                'format': 'json'
            }

            response = requests.get(url, params)
            json = response.json()

            coordinates_of_city = json['response']['GeoObjectCollection']['featureMember'][0]
            ['GeoObject']['Point']['pos'].split()

            long, lat = float(coordinates_of_city[0]), float(coordinates_of_city[1])
            return long, lat

        except Exception as e:
            status_error = e
            return

    return
