import json
import re
import time
import bs4
from ..Empty import Album, Singer, Song, Result, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Utils import net_get as _g, net2_session
from ..Utils import _MIN_TO_MM

_MUSIC_BD_SEARCH_HEADERS = {
    # ":authority": "music.taihe.com",
    # ":method": "GET",
    # ":path": "/search?word=%E8%BF%BD%E6%9C%88",
    # ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


class QianQian(object):
    def __init__(self):
        self.session = net2_session(["https://music.taihe.com/"])

    def _get_detail(self, id):
        tracklink = _g("https://music.taihe.com/v1/song/tracklink", data={
            "TSID": id,
            "timestamp": int(time.time()),
            "from": "webapp_music",
            "s_protocol": "1"
        })
        tracklink = json.loads(tracklink.text)
        return tracklink

    def search(self, _text, page=1, limit=20) -> Result:
        _p = page - 1 if page >= 1 else page
        try:
            res = _g("https://music.taihe.com/search?word=" + _text, headers=_MUSIC_BD_SEARCH_HEADERS)
            _bs4 = bs4.BeautifulSoup(res.text, "html.parser")
            _songs = _bs4.select(".search-content li.clearfix")
            songs = [Song({
                "id": str(_.select(".song a")[0]["href"]).replace("/song/", ""),
                "name": str(_.select(".song a")[0].text),
                "duration": _MIN_TO_MM(_.select(".time")[0].text),
                "subtitle": None,
                "album": BaseAlbum({
                    "id": str(_.select(".album a")[0]["href"]).replace("/album/", ""),
                    "name": _.select(".album a")[0].text,
                }),
                "singers": [Singer({
                    "id": str(__["href"]).replace("/artist/", ""),
                    "name": str(__.text),
                }) for __ in _.select(".artist a")],
            }) for _ in _songs]
            _data = SearchMusic({
                "songs": songs,
                "page": page,
                "limit": limit,
                "songCount": len(songs),
            })
            return Result(_data)
        except BaseException as base:
            print(base)
            return Result(None, False)

    def album(self, albumid) -> Result:
        try:
            res = _g("https://music.taihe.com/album/" + albumid).text
            _bs4 = bs4.BeautifulSoup(res, "html.parser")
            _songs = _bs4.select(".page-container.page-main li.clearfix")
            publishDate = _bs4.select("div.other")
            description = _bs4.select("div.intro")
            try:
                pic = str(re.findall(r'pic:"(.*?)",type', res)[0]).replace("\\u002F", "\\")
            except:
                pic = ""
            _data = Album({
                "id": albumid,
                "name": str(_bs4.select("h1.title")[0].text),
                "publishDate": re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', str(publishDate[0].text))[0] if len(
                    publishDate) >= 1 else "",
                "description": str(description[0].text) if len(description) >= 1 else "",
                "pics": [
                    pic,
                ],
                "singers": [{
                    "id": str(_["href"]).replace("/artist/", ""),
                    "name": str(_.text),
                } for _ in _bs4.select("span.artist a")],
                "songs": [Song({
                    "id": str(_.select(".song a")[0]["href"]).replace("/song/", ""),
                    "name": _.select(".song a")[0].text,
                    "subtitle": None,
                    "duration": _MIN_TO_MM(_.select(".time")[0].text),
                    "singer": [{
                        "id": str(_["href"]).replace("/artist/", ""),
                        "name": str(_.text),
                    } for _ in _.select(".artist a")]
                }) for _ in _songs],
            })
            return Result(_data)
        except:
            return Result(None, False)

    def detail(self, ids) -> Result:
        try:
            res = _g("https://music.taihe.com/v1/song/info",
                     data={"TSID": ids, "timestamp": int(time.time())})
            res = json.loads(res.text)
            res = res.get("data")[0]
            info = self._get_detail(res.get("assetId"))
            _data = MusicInfo({
                "id": res.get("assetId"),
                "name": info.get("data", {}).get("title", ""),
                "mp3_url": info.get("data", {}).get("path", ""),
                "music_url": None,
                "pics": [
                    info.get("data", {}).get("pic", "")
                ],
                "lyrics": [Lyric({"line": _[1],
                                  "time": _[0]}) for _ in
                           re.findall(r'\[([0-9]{2}:[0-9]{2}.[0-9]*?)\](.*?)\n', _g(res.get("lyric")).text)]
                if res.get("lyric") else res.get("lyric"),
                "singers": [Singer({
                    "id": _.get("artistCode"),
                    "name": _.get("name"),
                    "pics": [_.get("pic", "")]
                }) for _ in info.get("data", {}).get("artist", [])],
            })
            return Result(_data)
        except BaseException as base:
            # print(base)
            return Result(None, False)
