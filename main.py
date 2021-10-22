from vk_user import *
from ya_user import *

if __name__ == '__main__':
    VKTOKEN = # vk_token here
    YATOKEN = # ya_token here
    url_ = input('Введите url альбома: ')
    dir_input = input('Введите название папки, в которой будут храниться фото на вашем Yandex.Disk ')
    vk_client = VkUser(token=VKTOKEN, version='5.131')
    res = vk_client.get_response(url_)
    ya_client = YandexDiskUser(token=YATOKEN)
    ya_client.check_files()
    ya_client.mkdir_ya(dir_name=dir_input)
    ya_client.upload_photos(res, dir_name=dir_input)