import requests
from collections import namedtuple
from typing import List
import utils

StreamInfo = namedtuple("StreamInfo", ["title", "channel", "video_uuid"])

lives_URL = "https://api-sport-events.webservices.francetelevisions.fr/directs"
lives_info_url_template = "https://player.webservices.francetelevisions.fr/v1/videos/{" \
                          "video_uuid}?country_code=FR&w=453&h=255&version=5.10.7&domain=sport.francetvinfo.fr" \
                          "&device_type=desktop&browser=chrome" \
                          "&browser_version=74&os=windows&os_version=10.0&gmt=%2B1"

default_timeout = 5


def get_streams_list() -> List[StreamInfo]:
    """
    Retrieves the list of streams that are currently live from FranceTV API
    :return: A list of StreamInfo (named tuple)
    """
    try:
        streams_list_response = utils.get_nested_element_from_json_response(
            requests.get(lives_URL, timeout=default_timeout), "page", "lives")
    except RuntimeError:
        return []
    return [StreamInfo(stream["title"], stream["canal"], stream["sivideo-id"]) for stream in
            streams_list_response if "status" not in stream]


def get_authenticated_stream_url(video_uuid: str) -> str:
    """
    Retrieves an authenticated URL for the given video_uuid passed in parameter.
    :return: The authenticated URL which can be used to play the stream
    """
    stream_authentication_url = utils.get_nested_element_from_json_response(
        requests.get(lives_info_url_template.format(video_uuid=video_uuid), timeout=default_timeout), "video", "token")

    return utils.get_nested_element_from_json_response(requests.get(stream_authentication_url, timeout=default_timeout),
                                                       "url")
