from decouple import config
from multitoeter import MultiToeter, Twitter, Mastodon


def autoinit_multitoeter():
    mastodon = __init_mastodon()
    twitter = __init_twitter()

    toeters = {'mastodon': mastodon, 'twitter': twitter}
    toeters = {k: v for k, v in toeters.items() if v is not None}

    if len(toeters) == 0:
        raise ValueError('No backend could be selected')

    if len(toeters) == 1:
        # only use multitoeter if we have to
        return list(toeters.values)[0]

    return MultiToeter(toeters)


def __check_none_set(d: dict):
    return all([x is None for x in d.values()])


def __check_all_set(d: dict):
    missing = []
    for k, v in d.items():
        if v is None:
            missing.append(k)

    return missing


def __init_mastodon():
    cfg = dict(
       MASTODON_ACCESS_TOKEN=config('MASTODON_ACCESS_TOKEN', default=None),
       MASTODON_BASE_URL=config('MASTODON_BASE_URL', default=None),
    )

    if __check_none_set(cfg):
        return None

    missing = __check_all_set(cfg)
    if missing:
        [print(f'Missing config parameter for Mastodon: {v}') for v in missing]
        print('WARN: Disabled Mastodon due to missing config parameters')
        return None

    return Mastodon(cfg['MASTODON_ACCESS_TOKEN'], cfg['MASTODON_BASE_URL'])


def __init_twitter():
    cfg = dict(
       TWITTER_CONSUMER_KEY=config('TWITTER_CONSUMER_KEY', default=None),
       TWITTER_CONSUMER_SECRET=config('TWITTER_CONSUMER_SECRET', default=None),
       TWITTER_ACCESS_TOKEN=config('TWITTER_ACCESS_TOKEN', default=None),
       TWITTER_ACCESS_TOKEN_SECRET=config('TWITTER_ACCESS_TOKEN_SECRET', default=None),
    )

    if __check_none_set(cfg):
        return None

    missing = __check_all_set(cfg)
    if missing:
        [print(f'Missing config parameter for Twitter: {v}') for v in missing]
        print('WARN: Disabled Twitter due to missing config parameters')
        return None

    return Twitter(cfg['TWITTER_CONSUMER_KEY'], cfg['TWITTER_CONSUMER_SECRET'], cfg['TWITTER_ACCESS_TOKEN'], cfg['TWITTER_ACCESS_TOKEN_SECRET'])
