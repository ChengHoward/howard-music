import json
import re
import time
import uuid
import bs4
from ..Empty import Album, Singer, Song, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Empty import ResultSearchMusic, ResultAlbum, ResultMusicInfo
from ..Utils import net_get as _g, net2_session
from ..Utils import _MM_TO_MIN


class KuWo(object):
    def __init__(self):
        self.session = net2_session(["https://www.kuwo.cn/", ])

    def search(self, _text="", page=1, limit=20) -> ResultSearchMusic:
        _p = page - 1 if page >= 1 else page
        try:
            res = re.findall(r'^try\{var jsondata=(\{.*?\})\n;', _g("http://search.kuwo.cn/r.s", data={
                "all": _text,
                "pn": _p,
                "rn": limit,
                "httpsStatus": 1,
                "ft": "music",
                "client": "kt",
                "cluster": 0,
                "rformat": "json",
                "callback": "searchMusicResult",
                "encoding": "utf8",
                "r": int(time.time())
            }, headers={
                "Origin": "search.kuwo.cn",
                "Referer": "search.kuwo.cn",
                "Host": "search.kuwo.cn",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }).text)
            res = eval(res[0])
            _data = SearchMusic({
                "songs": [Song({
                    "id": str(_.get("MUSICRID")).replace("MUSIC_", ""),
                    "name": str(_.get("SONGNAME")).replace("&nbsp;"," "),
                    "duration": _.get("DURATION", 0),
                    "album": BaseAlbum({
                        "id": _.get("ALBUMID"),
                        "name": _.get("ALBUM").replace("&nbsp;"," "),
                    }),
                    "singers": [Singer({
                        "id": _.get("ARTISTID"),
                        "name": str(_.get("ARTIST")).replace("&nbsp;"," "),
                    })],
                }) for _ in res.get("abslist", [])],
                "page": page,
                "limit": limit,
                "songCount": int(res.get("TOTAL", 0)),
            })
            return ResultSearchMusic(_data)
        except:
            return ResultSearchMusic(None, False)

    def album(self, id) -> ResultAlbum:
        try:
            res = _g("http://search.kuwo.cn/r.s", data={
                "pn": "0",
                "rn": "1000",
                "stype": "albuminfo",
                "albumid": id,
                "alflac": "1",
                "pcmp4": "1",
                "encoding": "utf8",
                "vipver": "MUSIC_8.7.7.0_W4"
            }, headers={
                "Origin": "search.kuwo.cn",
                "Referer": "search.kuwo.cn",
                "Host": "search.kuwo.cn",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }).text
            res = eval(res)
            _data = Album({
                "id": res.get("albumid"),
                "name": res.get("name"),
                "publishDate": res.get("pub"),
                "description": res.get("info"),
                "pics": [
                    res.get("hts_img"),
                ],
                "singers": [Singer({
                    "id": res.get("artist"),
                    "name": res.get("name"),
                })],
                "songs": [Song({
                    "id": _.get("id"),
                    "name": _.get("name"),
                    "subtitle": _.get("subtitle"),
                    "singers": [Singer({
                        "id": res.get("artistid"),
                        "name": res.get("artist"),
                    })]
                }) for _ in res.get("musiclist")],
            })
            return ResultAlbum(_data)
        except BaseException as base:
            return ResultAlbum(None, state=False)

    def detail(self, id="") -> ResultMusicInfo:
        try:
            # 获取音乐地址
            res = _g("http://player.kuwo.cn/webmusic/st/getNewMuiseByRid?rid=MUSIC_" + id)
            _xml = bs4.BeautifulSoup(res.text, "html.parser")
            # 获取歌词信息
            res = _g("http://m.kuwo.cn/newh5/singles/songinfoandlrc", data={
                "musicId": id,
                "httpsStatus": 1,
                "reqId": str(uuid.uuid4())
            }, headers={
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Host": "m.kuwo.cn",
            })
            res = json.loads(res.text)
            data = res.get("data", {})
            lrclist = data.get("lrclist",[])
            try:
                mp3 = _xml.select("mp3dl")[0].text + _xml.select("mp3path")[0].text
            except:
                mp3 = ""
            try:
                aac = _xml.select("aacdl")[0].text + _xml.select("aacpath")[0].text
            except:
                aac = ""
            _data = MusicInfo({
                "id": data.get("songinfo", {}).get("id", ""),
                "name": str(data.get("songinfo", {}).get("songName", "")).replace("&nbsp;"," "),
                "mp3_url": mp3,
                "music_url": aac,
                "pics": [
                    data.get("songinfo", {}).get("pic", None),
                ],
                "lyrics": [Lyric({"line": _.get("lineLyric", ""),
                                  "time": _MM_TO_MIN(_.get("time", ""))}) for _ in
                           lrclist],
                "singers": [Singer({
                    "id": data.get("songinfo", {}).get("artistId",""),
                    "name": data.get("songinfo", {}).get("artist",""),
                    "pics": [data.get("songinfo", {}).get("pic", "")]
                })],
            })
            return ResultMusicInfo(_data)
        except:
            return ResultMusicInfo(None, False)
