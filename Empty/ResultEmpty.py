from Empty.SearchEmpty import SearchMusic
from Empty.AlbumEmpty import Album
from Empty.BaseEmpty import BaseEmpty
from Empty.MusicInfoEmpty import MusicInfo


class Result(BaseEmpty):
    def __init__(self, data, state=True):
        self.state: bool = state
        self.data: object = data


class ResultSearchMusic(BaseEmpty):
    def __init__(self, data, state=True):
        self.state: bool = state
        self.data: SearchMusic = data


class ResultAlbum(BaseEmpty):
    def __init__(self, data, state=True):
        self.state: bool = state
        self.data: Album = data


class ResultMusicInfo(BaseEmpty):
    def __init__(self, data, state=True):
        self.state: bool = state
        self.data: MusicInfo = data
