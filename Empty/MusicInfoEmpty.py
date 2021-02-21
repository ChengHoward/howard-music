from Empty.LyricEmpty import Lyric
from Empty.BaseEmpty import BaseEmpty
from Empty.SingerEmpty import Singer


class MusicInfo(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.id: str = _dic.get("id","")
        self.name: str = _dic.get("name","")
        self.mp3_url: str = _dic.get("mp3_url","")
        self.music_url: str = _dic.get("music_url","")
        self.lyrics: list[Lyric] = _dic.get("lyrics",[])
        self.pics: list[str] = _dic.get("pics", [])
        self.singers: list[Singer] = _dic.get("singers", [])