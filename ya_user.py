import requests
from progress.bar import IncrementalBar
import time
import json

class YandexDiskUser:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def check_files(self):
        check_list = []
        url = self.url + 'files'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            for item in response.json()['items']:
                check_list.append(item['name'])
        return check_list

    def mkdir_ya(self, dir_name):
        params = {'path': dir_name}
        response = requests.put(self.url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f'Папка {dir_name} создана на вашем Яндекс.Диске')
        return dir_name

    def upload_photos(self, response, dir_name):
        template = []
        for k in response['response']['items']:
            template.append({
                'file_name': str(k['likes']['count']),
                'size': k['sizes'][-1]['type'],
                'download_url': k['sizes'][-1]['url']
            })
        url = self.url + 'upload'
        bar = IncrementalBar('Фотографий загружено', max=len(template))
        for item in template:
            if item['file_name'] in self.check_files():
                item['file_name'] += '_'
            response = requests.post(url=url, headers=self.headers, params={'path': dir_name + '/' + item['file_name'], 'url': item['download_url']})
            del item['download_url']
            bar.next()
            time.sleep(.1)
        bar.finish()
        with open(dir_name + '_bp.json', 'w') as outfile:
            json.dump(template, outfile)
        print(f'На ваш Яндекс.диск успешно загружено {len(template)} фотографий')