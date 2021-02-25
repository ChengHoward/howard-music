import json
import re
import time
from ..Empty import Album, Singer, Song, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Empty import ResultSearchMusic, ResultAlbum, ResultMusicInfo
from ..Utils import net2_session

_MUSIC_KG_SEARCH_PARAMS = {
    "callback": "callback123",
    "bitrate": "0",
    "isfuzzy": "0",
    "tag": "em",
    "inputtype": "0",
    "platform": "WebFilter",
    "userid": "-1",
    "clientver": "2000",
    "iscorrection": "1",
    "privilege_filter": "0",
    "srcappid": "2919",
    "clienttime": "1607052381011",
    "mid": "1607052381011",
    "uuid": "1607052381011",
    "dfid": "-",
    "signature": "2BD0F5EAD22C26C4FAF54ABEA736D1BD",
}
_MUSIC_KG_SEARCH_HEADERS = {
    "referer": "http://m.kugou.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46"
                  + " (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
_MUSIC_KG_DOWNLOAD_HEADERS = {
    ":authority": "wwwapi.kugou.com",
    ":method": "GET",
    ":scheme": "https",
}
_MUSIC_KG_ALBUM_HEADERS = {
    ":authority": "m3ws.kugou.com",
    ":method": "GET",
    ":scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "referer": "https://m3ws.kugou.com/album/14456909.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}


class KuGou(object):
    def __init__(self):
        self.session = net2_session(["http://m.kugou.com/", "https://m3ws.kugou.com/"])

    def search(self, _text="", page=1, limit=30) -> ResultSearchMusic:
        # `ID ` use 'hash`
        try:
            _MUSIC_KG_SEARCH_PARAMS.update({
                "keyword": _text,
                "page": page,
                "pagesize": limit,
            })
            res = self.session.get("http://songsearch.kugou.com/song_search_v2",
                                   params={'keyword': _text,
                                           'platform': 'WebFilter',
                                           'format': 'json',
                                           'page': page,
                                           'pagesize': limit},
                                   headers=_MUSIC_KG_SEARCH_HEADERS).text
            res = eval(res)
            _data = SearchMusic({
                "songs": [Song({
                    "id": _.get("FileHash"),
                    "name": _.get("SongName"),
                    "duration": _.get("Duration", 0),
                    "subtitle": _.get("OriSongName", ""),
                    "album": BaseAlbum({
                        "id": _.get("AlbumID"),
                        "name": _.get("AlbumName"),
                    }),
                    "singers": [Singer({
                        "id": id,
                        "name": name,
                    }) for id, name in zip(_.get("SingerId"), str(_.get("SingerName", "")).split("、"))],
                }) for _ in res.get("data", {}).get("lists", [])],
                "page": page,
                "limit": limit,
                "songCount": res.get("data", {}).get("total", 0),
            })
            return ResultSearchMusic(_data)
        except:
            return ResultSearchMusic(None, False)

    def album(self, albumid) -> ResultAlbum:
        try:
            _MUSIC_KG_ALBUM_HEADERS.update({"referer": "https://m3ws.kugou.com/album/" + albumid + ".html"})
            res = self.session.get("https://m3ws.kugou.com/app/i/getablum.php", params={
                "type": 1,
                "ablumid": albumid
            }, headers=_MUSIC_KG_ALBUM_HEADERS).text
            res = eval(res)
            _data = Album({
                "id": albumid,
                "name": res.get("cname"),
                "publishDate": res.get("publish_date"),
                "description": res.get("intro"),
                "pics": [
                    res.get("img400"),
                    res.get("img"),
                ],
                "singers": [Singer({
                    "id": res.get("singerid"),
                    "name": res.get("singer"),
                })],
                "songs": [Song({
                    "id": _.get("hash", ""),
                    "name": _.get("songname"),
                    "subtitle": _.get("subtitle"),
                    "duration": _.get("Duration", 0),
                    "singers": [Singer({
                        "id": res.get("singerid"),
                        "name": res.get("singer"),
                    })]
                }) for _ in res.get("list")],
            })
            return ResultAlbum(_data)
        except BaseException as base:
            return ResultAlbum(None, state=False)

    def detail(self, hash, albumid) -> ResultMusicInfo:
        # MUSIC_XXXXXXXX hash
        try:
            # 获取音乐地址
            res = self.session.get("https://wwwapi.kugou.com/yy/index.php", params={
                "r": "play/getdata",
                "callback": "jQuery191030029284036250337_1607159310710",
                "hash": hash,
                "dfid": "",
                "mid": "00324ae2e621013f4c8c211113dd7016",
                "platid": "",
                "album_id": albumid,
                "_": int(time.time())
            })
            res = re.findall(r'^jQuery191030029284036250337_1607159310710\((.*?)\);$', res.text)
            res = json.loads(res[0])
            lrc = res.get("data", {}).get("lyrics", [])
            _data = MusicInfo({
                "id": hash,
                "name": res.get("data", {}).get("song_name", ""),
                "mp3_url": res.get("data", {}).get("play_url", ""),
                "music_url": res.get("data", {}).get("play_backup_url", None),
                "pics": [
                    res.get("data", {}).get("img", None),
                ],
                "lyrics": [Lyric({"line": _[1],
                                  "time": _[0]}) for _ in
                           re.findall(r'\[([0-9]{2}:[0-9]{2}.[0-9]*?)\](.*?)\n', lrc)],
                "singers": [Singer({
                    "id": _.get("author_id"),
                    "name": _.get("author_name"),
                    "pics":[_.get("avatar","")]
                }) for _ in res.get("data",{}).get("authors",[])],
            })
            return ResultMusicInfo(_data)
        except:
            return ResultMusicInfo(None, False)
