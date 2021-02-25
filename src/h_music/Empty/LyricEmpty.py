from ..Empty.BaseEmpty import BaseEmpty


class Lyric(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.line: str = _dic.get("line","")
        self.time: str = _dic.get("time","")