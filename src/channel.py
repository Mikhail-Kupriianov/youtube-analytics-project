import os
from googleapiclient.discovery import build


import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id  # - id канала
        self.channel_info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.dict_to_print = None
        self.title = self.channel_info.get('items', {})[0].get('snippet', {}).get('title')  # - название канала
        self.description = self.channel_info.get('items', {})[0].get('snippet', {}).get('description')  # - описание
        self.url = self.channel_info.get('items', {})[0].get('snippet', {}).get('thumbnails', {}).get('default',
                                                                                                      {}).get(
            'url')  # - ссылка на канал
        self.subscriber_count = self.channel_info.get('items', {})[0].get('statistics', {}).get(
            'subscriberCount')  # - количество подписчиков
        self.video_count = self.channel_info.get('items', {})[0].get('statistics', {}).get(
            'videoCount')  # - количество видео
        self.view_count = self.channel_info.get('items', {})[0].get('statistics', {}).get(
            'viewCount')  # - общее количество просмотров

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        """ Возвращает id канала"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, chanel_id):
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    def printj(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        self.dict_to_print = dict_to_print
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.printj(channel)

    def to_json(self, file_name):
        #  json_object = json.dumps(self.channel_info, ensure_ascii=False, indent=4)
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(self.channel_info, file, ensure_ascii=False, sort_keys=False, indent=4)
