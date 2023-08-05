# 📢 MultiToeter
## Introduction
MultiToeter is a python library providing a simplified unified API for sending messages to both the Twitter and Mastodon platform at the same time.

## Usage
```bash
# install through pip
pip install multitoeter
```

### Initialize through autoinit
MultiToeter support initializing your keys and secrets, needed for connecting to the Twitter and Mastodon API, through environment variables or through a `.env` file. Below are two examples on how to use this. You can mix and match these two methods. The priority is currently to try environment variables first followed by the `.env` file.

```python3
# Simple script to send a message through MultiToeter
# Save as: test.py
from multitoeter import autoinit_multitoeter

mt = autoinit_multitoeter()

toeter = mt.toeter('Testing MultiToeter API autoinit')
toeter = mt.toeter('Reply message', in_reply_to=toeter)
```

```bash
# environment variable example
# only use mastodon in this example
MASTODON_ACCESS_TOKEN=<..> MASTODON_BASE_URL=https://mstdn.science python test.py 
```

```bash
# .env file example
MASTODON_ACCESS_TOKEN=<..>
MASTODON_BASE_URL=https://mstdn.science

TWITTER_CONSUMER_KEY=<..>
TWITTER_CONSUMER_SECRET=<..>
TWITTER_ACCESS_TOKEN=<..>
TWITTER_ACCESS_TOKEN_SECRET=<..>

# Now run test.py:
# python test.py 
```



### Initialize in code
A secondary approach is to initialize MultiToeter in code instead of using the autoinit. This gives you more flexibility and allows you to use more than one account for the same platform should you need it.

```python3
from multitoeter import Mastodon, Twitter, MultiToeter

mastodon1 = Mastodon(
  access_token="<..>",
  api_base_url="https://mstdn.science"
)
mastodon2 = Mastodon(
  access_token="<..>",
  api_base_url="https://mstdn.social/"
)

twitter1 = Twitter(
  consumer_key="<..>"
  consumer_secret="<..>"
  access_token="<..>"
  access_token_secret="<..>"
)

multi = MultiToeter({'mastodon1': mastodon1, 'mastodon2': mastodon2, 'twitter': twitter1})

toeter = multi.toeter("Test post via MultiToeter API")
toeter = multi.toeter("Test reply via MultiToeter API", in_reply_to=toeter)
```


### Adding media files
Limited support for media files is available. The unified API expects you to point to the media files directly.

```python3
# Assume that the file test.jpg exists
from multitoeter import autoinit_multitoeter

mt = autoinit_multitoeter()

toeter = mt.toeter('Testing MultiToeter API autoinit', media_files=['test.jpg'])
```
