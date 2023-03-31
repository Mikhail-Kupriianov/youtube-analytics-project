import datetime
import os
import json
import isodate
from googleapiclient.discovery import build
from src.video import Video


class PlayList:
    """Класс для плейлиста ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.list_playlist: dict = self.youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.title = self.list_playlist.get('items', {})[0].get('snippet', {}).get('title')
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()

    @property
    def total_duration(self):
        """Возвращает длительность всех видео для плейлиста"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        result = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            result += isodate.parse_duration(iso_8601_duration)
        return result

    def show_best_video(self) -> str:
        statistic_list = []
        for video in self.playlist_videos['items']:
            video_id = str(video['contentDetails']['videoId'])
            statistic_list.append([video_id, int(Video(video_id).like_count)])

        return "https://youtu.be/" + "".join([x[0] for x in statistic_list
                                              if x[1] == max([x[1] for x in statistic_list])])


# if __name__ == '__main__':
#     pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
#     pl.show_best_video()
#     print(pl.list_playlist, '\n')
#     print(pl.list_playlist.get('items', {})[0].get('snippet', {}).get('title'))
#     print(json.dumps(pl.list_playlist, indent=4, ensure_ascii=False))
#     playlist_videos1 = pl.youtube.playlistItems().list(playlistId=pl.playlist_id,
#                                                        part='contentDetails',
#                                                        maxResults=50,
#                                                        ).execute()
#     print(json.dumps(playlist_videos1, indent=4, ensure_ascii=False))
#     video_ids1: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos1['items']]
#     print(video_ids1)
#     video_response1 = pl.youtube.videos().list(part='contentDetails,statistics',
#                                                id=','.join(video_ids1)
#                                                ).execute()
#     print(video_response1)
#     list_all_durations = []  # [isodate.parse_duration(video['contentDetails']['duration']) for video in video_response]
#     for video in video_response1['items']:
#         # YouTube video duration is in ISO 8601 format
#         iso_8601_duration_1 = video['contentDetails']['duration']
#         duration = isodate.parse_duration(iso_8601_duration_1)
#         list_all_durations.append(duration)
#     print(list_all_durations)
