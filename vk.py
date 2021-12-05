



class VK_request:

    def __init__(self, token_list, id, username,   version='5.131'):
        self.token = token_list[0]
        self.user_id = id
        self.username = username
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()

    #  Функция получения данных по логину, метод users.get
    def user_get(self, user_ids):
        user_url = self.url + 'users.get'
        self.user_ids = user_ids
        self.user_params = {
            'user_ids': self.user_ids,
            'fields': 'id'
        }
        try:
            req = requests.get(user_url, params={**self.params, **self.user_params}).json()
        except Exception as error:
            print('Убедитесь в верном токене логине. ')
            return 'Убедитесь в верном токене логине. {error}'
        if 'error' in req:
            print('Неверный логин')
        return req.get('response')[0].get('id')

    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']

    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_dpi(photo_items[i]['sizes'])
            time_warp = time_convert(photo_items[i]['date'])

            new_value = result.get(likes_count, [])
            new_value.append({'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict
