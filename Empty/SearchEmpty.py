from Empty.SongEmpty import  Song
from Empty.BaseEmpty import  BaseEmpty


class SearchMusic(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.songs: list[Song] = _dic.get("songs", [])
        self.page: int = _dic.get("page", 1)
        self.limit: int = _dic.get("limit", 20)
        self.songCount: int = _dic.get("songCount", 0)
