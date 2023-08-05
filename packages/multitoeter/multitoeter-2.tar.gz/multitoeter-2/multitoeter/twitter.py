import tweepy

from multitoeter.unifiedapi import AbstractToeter


class Twitter(AbstractToeter):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

    def toeter(self, message, media_files=None, in_reply_to=None):
        media_ids = []
        if media_files is not None:
            media_ids = [self._api.media_upload(media_file) for media_file in media_files]

        if in_reply_to is not None:
            return self._api.update_status(
                    message,
                    media_ids=[media.media_id for media in media_ids],
                    in_reply_to_status_id=in_reply_to.id, auto_populate_reply_metadata=True
            )
        return self._api.update_status(message, media_ids=[media.media_id for media in media_ids])
