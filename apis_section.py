from googleapiclient.discovery import build


class YoutubeAPI:
    DEFAULT_API_KEY = 'AIzaSyC_Z02oQ6JsYr839X9BzXWzS3L9cw2-rxg'

    def __init__(self, api_key: object = None):
        if api_key is None:
            api_key = self.DEFAULT_API_KEY
        self.api_key = api_key

    def get_service(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        return youtube

    def get_api_key(self):
        return self.api_key
