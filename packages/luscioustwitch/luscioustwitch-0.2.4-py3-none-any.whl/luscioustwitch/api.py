from .saferequests import *

TWITCH_API_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class TwitchAPI:
  API_URL = "https://api.twitch.tv/helix"
  CLIENT_ID = ""
  CLIENT_SECRET = ""
  DEFAULT_HEADERS = {}
  REQ = RateLimitedRequests(400, 60)

  def __init__(self, credentials):
    """Constructor for TwitchAPI. Must pass in credentials in the form of a dictionary.

    Args:
        credentials (dict): API Credentials. "CLIENT_ID" and "CLIENT_SECRET" should be in the dict.
    """
    self.CLIENT_ID = credentials["CLIENT_ID"]
    self.CLIENT_SECRET = credentials["CLIENT_SECRET"]
    self.DEFAULT_HEADERS = { "Authorization": f"Bearer {self.CLIENT_SECRET}", "Client-Id": self.CLIENT_ID }

  def get_user_id(self, username):
    """Get user ID from username.

    Args:
        username (string): Username

    Returns:
        string: User ID
    """
    url = f"{self.API_URL}/users?login={username}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r["data"][0]["id"]
    except:
      return ""
  
  def get_channel_info(self, user_id):
    """Get Channel Information.

    Args:
        user_id (string): User ID

    Returns:
        dict: Channel information
    """
    url = f"{self.API_URL}/channels?broadcaster_id={user_id}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data']
    except:
      return None
      
  def get_category_id(self, category_name):
    """Get category ID from category name

    Args:
        category_name (string): Category name

    Returns:
        string: Category ID
    """
    url = f"{self.API_URL}/games?name={category_name}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r["data"][0]["id"]
    except:
      return None

  def get_clip(self, clip_id):
    """Get info for one clip from ID.

    Args:
        clip_id (string): Video ID

    Returns:
        dict: clip info
    """
    url = f"{self.API_URL}/clips?id={clip_id}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data'][0]
    except:
      return None
  
  def __add_parameters(self, url, params):
    """Add parameters to an API request URL.

    Args:
        url (string): API endpoint
        params (string): Dictionary of parameters. See function descriptions for valid params.

    Returns:
        string: URL with params.
    """
    separator = "?"
    for k, v in params.items():
      url += f"{separator}{k}={v}"
      separator = "&"
    return url

  def get_clips(self, params):
    """Get clips based on params.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Clip ID
            broadcaster_id (string): Broadcaster ID
            game_id (string): Game/Category ID
            started_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            ended_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            first (int): fetch the first n clips
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of clip info
    """
    url = f"{self.API_URL}/clips"
    url = self.__add_parameters(url, params)
    
    r = self.REQ.safe_get(url = url, headers=self.DEFAULT_HEADERS)
    
    try:
      return r['data'], r['pagination']['cursor']
    except:
      try:
        return r['data'], ""
      except:
        return [], ""

  def get_all_clips(self, params):
    """Get all clips based on params (auto-pagination).

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Clip ID
            broadcaster_id (string): Broadcaster ID
            game_id (string): Game/Category ID
            started_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            ended_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            first (int): fetch the first n clips
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of clip info
    """
    all_clips = []
    while True:
      clips, cursor = self.get_clips(params)

      for clip in clips:
        all_clips.append(clip)
      
      if cursor == "":
        return all_clips
      else:
        params["after"] = cursor

  def get_video(self, video_id):
    """Get info for one video from ID.

    Args:
        video_id (string): Video ID

    Returns:
        dict: Video info
    """
    url = f"{self.API_URL}/videos?id={video_id}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data'][0]
    except:
      return None

  def get_videos(self, params):
    """Get videos based on params.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Video ID
            user_id (string): User ID
            game_id (string): Game/Category ID
            language (string): ISO 639-1
            period (string): "all", "day", "month", or "week"
            sort (string): "time", "trending", or "views"
            type (string): "all", "archive", "highlight", or "upload"
            first (int): fetch the first n videos
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of video info
        string: Pagination cursor
    """
    url = f"{self.API_URL}/videos"
    url = self.__add_parameters(url, params)
    
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data'], r['pagination']['cursor']
    except:
      try:
        return r['data'], ""
      except:
        return [], ""

  def get_all_videos(self, params):
    """Get all videos based on params (auto-pagination).

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Video ID
            user_id (string): User ID
            game_id (string): Game/Category ID
            language (string): ISO 639-1
            period (string): "all", "day", "month", or "week"
            sort (string): "time", "trending", or "views"
            type (string): "all", "archive", "highlight", or "upload"
            first (int): fetch the first n videos
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of video info
    """
    all_clips = []
    while True:
      vids, cursor = self.get_videos(params)

      for vod in vids:
        all_clips.append(vod)
      
      if cursor == "":
        return all_clips
      else:
        params["after"] = cursor

  def get_streams(self, params):
    """Get a list of streams.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            user_id (string): User ID
            user_login (string): Username
            game_id (string): Game/Category ID
            type (string): "all" or "live"
            language (string): ISO 639-1
            first (int): fetch the first n streams
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of stream info
    """
    url = f"{self.API_URL}/streams/"
    url = self.__add_parameters(url, params)
    
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data']
    except:
      return []

  def is_broadcaster_live(self, broadcaster_id = ""):
    bid = broadcaster_id if broadcaster_id != "" else self.DEFAULT_BROADCASTER_ID
    stream_info = self.get_streams({ "user_id": bid })
    return (len(stream_info) > 0)
  
  def get_emotes(self, user_id):
    """Get Channel Emotes

    Args:
        user_id (string): User ID

    Returns:
        list: List of emote information.
    """
    url = f"{self.API_URL}/chat/emotes?broadcaster_id={user_id}"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data']
    except:
      return []
  
  def get_global_emotes(self):
    """Get Global Emotes.

    Returns:
        list: List of global emote information.
    """
    url = f"{self.API_URL}/chat/emotes/global"
    r = self.REQ.safe_get(url = url, headers = self.DEFAULT_HEADERS)
    
    try:
      return r['data']
    except:
      return []