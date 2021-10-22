import requests

class VkUser:

    url = 'https://api.vk.com/method/photos.get'

    def __init__(self, token, version):

        self.params = {
            'access_token': token,
            'v': version
        }

    def _get_id():
        album_input = url.split('/')[-1].split('_')[1]
        id_vk = url.split('/')[-1].split('_')[0].replace('album', '')

    def get_response(self, input_url):
        album = input_url.split('/')[-1].split('_')[1]
        id_vk = input_url.split('/')[-1].split('_')[0].replace('album', '')
        if album == '0':
            album = 'profile'
        elif album == '00':
            album = 'wall'
        elif album == '000':
            album = 'saved'
        else:
            pass
        get_json_params = {
            'owner_id': id_vk,
            'album_id': album,
            'extended': '1',
        }
        response = requests.get(self.url, params={**self.params, **get_json_params})
        if response.status_code == 200:
            return response.json()