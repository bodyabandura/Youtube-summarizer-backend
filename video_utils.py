from pytubefix import YouTube
from config import _ERROR
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


def get_video_id_from_url(url):
    try:
        # parsed_url = urllib.parse.urlparse(url)
        # return urllib.parse.parse_qs(parsed_url.query)['v'][0]
        return url.strip().split('=')[1]
    except Exception as e:
        print(f"{_ERROR}\n{e}")

    # return url.split('=')[1]
    # context = ssl.create_default_context(cafile=certifi.where())
    # parsed_url = urllib.parse.urlparse(url)
    # with urllib.request.urlopen(url, context=context) as response:
    #     content = response.read()
    # return urllib.parse.parse_qs(parsed_url.query)['v'][0]


def get_video_title(url):
    try:
        return YouTube(url).title
    except Exception as e:
        print(f"{_ERROR}\n{e}")


def get_video_thumbnail(url):
    try:
        print("9.1")
        return YouTube(url).thumbnail_url
    except Exception as e:
        print(f"{_ERROR}\n{e}")
