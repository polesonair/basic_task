import os
import requests
import datetime
from vk import *
from yandex import *


def get_token_id(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as token_file:
        token = token_file.readline().strip()
        id = token_file.readline().strip()
    return [token, id]

def find_max_dpi(dict_in_search):
    max_dpi = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            necessary = j
    return dict_in_search[necessary].get('url'), dict_in_search[necessary].get('type')

def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    string_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return string_time

if __name__ == “__main__”:

    def get_params():
        id = 0
        username = ''
        photo_count = 0
        id_username = ''

        while not id_username:
            print('Enter prefer id or username:')
            id_username = input()
            if id_username.isdigit():
                id = int(id_username)
                break
            else:
                username = id_username
                break
            print('Input incorrect!')

        while not photo_count:
            print('Enter prefer photo count:')
            photo_count = input()
            if photo_count.isdigit() and photo_count > 0:
                break
            print('Input incorrect!')

        return id, username, photo_count


    id, username, photo_count = get_params()

    tokenVK = 'tokenVK.txt'
    tokenYandex = 'tokenYa.txt'

    my_VK = VK_request(get_token_id(tokenVK), id, username)
    print(my_VK.json)

    my_yandex = Yandex('VK photo copies', get_token_id(tokenYandex))
    my_yandex.create_copy(my_VK.export_dict)