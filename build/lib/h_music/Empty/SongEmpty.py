from ..Empty.BaseAlbumEmpty import BaseAlbum
from ..Empty.SingerEmpty import Singer
from ..Empty.BaseEmpty import BaseEmpty

class Song(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.id: str = _dic.get("id","")
        self.oid: str = _dic.get("oid",None)
        self.name: str = _dic.get("name","")
        self.subtitle: str = _dic.get("subtitle","")
        self.duration: int = _dic.get("duration",0)
        self.album: BaseAlbum = _dic.get("album",None)
        self.privilege: bool = _dic.get("privilege",False)
        self.singers: list[Singer] = _dic.get("singers",[])
