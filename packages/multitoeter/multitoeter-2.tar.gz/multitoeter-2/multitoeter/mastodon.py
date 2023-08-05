from mastodon import Mastodon as Mas

from multitoeter.unifiedapi import AbstractToeter


class Mastodon(AbstractToeter):
    def __init__(self, access_token, api_base_url):
        self._api = Mas(access_token=access_token, api_base_url=api_base_url)

    def toeter(self, message, media_files=None, in_reply_to=None):
        media_ids = []
        if media_files is not None:
            media_ids = [self._api.media_post(media_file) for media_file in media_files]

        if in_reply_to is not None:
            return self._api.status_post(message, media_ids=[media['id'] for media in media_ids], in_reply_to_id=in_reply_to['id'])
        return self._api.status_post(message, media_ids=[media['id'] for media in media_ids])
