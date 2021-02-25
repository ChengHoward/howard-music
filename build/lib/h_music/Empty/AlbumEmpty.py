from ..Empty.SongEmpty import Song
from ..Empty.BaseAlbumEmpty import BaseEmpty
from ..Empty.SingerEmpty import Singer


class Album(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.id = _dic.get("id", "")
        self.name = _dic.get("name", "")
        self.publishDate = _dic.get("publishDate", "")
        self.description = _dic.get("description", "")
        self.pics: list[str] = _dic.get("pics", [])
        self.songs: list[Song] = _dic.get("songs", [])
        self.singers: list[Singer] = _dic.get("singers", [])
