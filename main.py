import requests
from progress.bar import IncrementalBar
import time
import json
from pprint import pprint

def check_files(yatoken):
    check_list = []
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}' .format(yatoken)
    }

    url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for item in response.json()['items']:
            check_list.append(item['name'])
    return check_list


def mkdir_ya(yatoken, dir_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}' .format(yatoken)
    }

    params = {'path': dir_name}

    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    response = requests.put(url, headers=headers, params=params)
    if response.status_code == 201:
        print(f'Папка {dir_name} создана на вашем Яндекс.Диске')
    return dir_name

def get_photos(vktoken, version):
    params = {
        'access_token': vktoken,
        'v': version,
        'owner_id': id_vk,
        'album_id': 'profile',
        'extended': '1',
    }

    url = 'https://api.vk.com/method/photos.get'
    response = requests.get(url, params=params).json()
    template = []
    for k in response['response']['items']:
        template.append({
            'file_name': str(k['likes']['count']),
            'size': k['sizes'][-1]['type'],
            'download_url': k['sizes'][-1]['url']
        })
    return template


def upload_photos(yatoken):
    dir_name = mkdir_ya(yatoken, id_vk)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(yatoken)
    }

    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    template = get_photos(vktoken_, '5.131')
    bar = IncrementalBar('Фотографий загружено', max=len(template))
    for item in template:
        if item['file_name'] in check_files(yatoken_):
            item['file_name'] += '_again'
        response = requests.post(url=url, headers=headers,
                                 params={'path': dir_name + '/' + item['file_name'], 'url': item['download_url']})
        del item['download_url']
        bar.next()
        time.sleep(.1)
    bar.finish()
    with open('photo_backup.json', 'w') as outfile:
        json.dump(template, outfile)
    print(f'На ваш Яндекс.диск успешно загружено {len(template)} фотографий')


if __name__ == '__main__':
    with open('vktoken') as f:
        vktoken_ = f.read().strip()

id_vk = input('Введите id пользователя vk в числовой форме\n')
yatoken_ = input('Ввидеите token Яндекс.Диска ')

upload_photos(yatoken_)