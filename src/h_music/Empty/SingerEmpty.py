from ..Empty.BaseEmpty import BaseEmpty

class Singer(BaseEmpty):
    def __init__(self, _dic=None):
        if _dic is None:
            _dic = {}
        self.id = _dic.get("id","")
        self.name = _dic.get("name","")
        self.pics: list[str] = _dic.get("pics",[])
