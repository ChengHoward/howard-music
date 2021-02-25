import base64
import json
import re
import bs4
from ..Empty import Album, Singer, Song, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Empty import ResultSearchMusic, ResultAlbum, ResultMusicInfo
from ..Utils import net_get as _g, net2_session

_MUSIC_QQ_DOWNLOAD_HEADERS = {
    # ":authority": "u.y.qq.com",
    # ":method": "GET",
}
_MUSIC_QQ_SEARCH_HEADERS = {
    "Accept": "application/json,text/plain,*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    "Host": "i.y.qq.com",
    "Origin": "http://y.qq.com/",
    "Referer": "http://y.qq.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}
_MUSIC_QQ_SEARCH_PARAMS = {
    "g_tk": "938407465",
    "uin": "0",
    "format": "jsonp",
    "inCharset": "utf-8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "h5",
    "needNewCode": "1",
    "zhidaqu": "1",
    "catZhida": "1",
    "t": "0",
    "flag": "1",
    "ie": "utf-8",
    "sem": "1",
    "aggr": "0",
    "remoteplace": "txt.mqq.all",
    "jsonpCallback": "json",
}
_MUSIC_QQ_DOWNLOAD_LYRIC_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    "Host": "i.y.qq.com",
    "Origin": "http://y.qq.com/",
    "Referer": "http://y.qq.com/",
    "from": "webapp_music",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}
_MUSIC_QQ_DOWNLOAD_LYRIC_PARAMS = {
    "songmid": "",
    "loginUin": "0",
    "hostUin": "0",
    "format": "jsonp",
    "inCharset": "GB2312",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "yqq",
    "jsonpCallback": "MusicJsonCallback",
    "needNewCode": "0",
}


def DEF_MUSIC_QQ_DOWNLOAD_DATA(id):
    return {
        "loginUin": 0,
        "hostUin": 0,
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf-8",
        "notice": 0,
        "platform": "yqq.json",
        "needNewCode": 0,
        "data": json.dumps({
            "req_0": {
                "module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                "param": {
                    "guid": "10000",
                    "songmid": [id],
                    "songtype": [0],
                    "uin": "0",
                    "loginflag": 1,
                    "platform": "20"}},
            "comm": {
                "uin": 0,
                "format": "json",
                "ct": 20,
                "cv": 0
            }
        }, ensure_ascii=False)
    }


class QQ(object):
    def __init__(self):
        self.session = net2_session(["https://y.qq.com/",])

    def search(self, _text="", page=1, limit=20) -> ResultSearchMusic:
        _MUSIC_QQ_SEARCH_PARAMS.update({
            "perpage": limit,
            "n": limit,
            "p": page,
            "w": _text,
        })
        try:
            res = re.findall(r'^json\((.*?)\)$',
                             _g("http://i.y.qq.com/s.music/fcgi-bin/search_for_qq_cp",
                                data=_MUSIC_QQ_SEARCH_PARAMS,
                                headers=_MUSIC_QQ_SEARCH_HEADERS).text)
            res = json.loads(res[0])
            songs = res.get("data", {}).get("song", {}).get("list", [])
            _data = SearchMusic({
                "songs": [Song({
                    "id": _.get("songmid"),
                    "name": _.get("songname"),
                    "duration": _.get("interval", 0),
                    "subtitle": _.get("songname_hilight", ""),
                    "album": BaseAlbum({
                        "id": _.get("albummid"),
                        "name": _.get("albumname"),
                    }),
                    "singers": [Singer({
                        "id": __.get("mid"),
                        "name": __.get("name"),
                    }) for __ in _.get("singer")],
                }) for _ in songs],
                "page": page,
                "limit": limit,
                "songCount": res.get("data", {}).get("song", {}).get("totalnum", 0)
            })
            return ResultSearchMusic(_data)
        except:
            return ResultSearchMusic(None, False)

    def album(self, albumid) -> ResultAlbum:
        try:
            content = _g(
                "https://i.y.qq.com/n2/m/share/details/album.html?ADTAG=newyqq.album&source=ydetail&albummid=" + albumid).text
            body = self.session.get("https://y.qq.com/n/yqq/album/" + albumid + ".html").text
            res = re.findall(r'<script>var firstPageData = (.*?)</script>\n', content)
            res = eval(res[0])
            imgs = bs4.BeautifulSoup(body, "html.parser").select("#albumImg")
            img = imgs[0]['src'] if len(imgs) else ""
            albumData = res.get("albumData", {})
            _data = Album({
                "id": albumData.get("albumMid"),
                "name": albumData.get("albumName"),
                "publishDate": albumData.get("publishDate"),
                "description": albumData.get("desc"),
                "pics": [
                    img,
                ],
                "singers": [Singer({
                    "id": albumData.get("singer", {}).get("mid", ""),
                    "name": albumData.get("singer", {}).get("name", ""),
                })],
                "songs": [Song({
                    "id": _.get("songInfo").get("mid"),
                    "name": _.get("songInfo").get("name"),
                    "subtitle": _.get("songInfo").get("title"),
                    "duration": _.get("interval", 0),
                    "singers": [Singer({
                        "id": __.get("mid"),
                        "name": __.get("name"),
                    }) for __ in _.get("songInfo", {}).get("singer", [])]
                }) for _ in albumData.get("list")],
            })
            return ResultAlbum(_data)
        except BaseException as base:
            return ResultAlbum(None, False)

    def detail(self, id="") -> ResultMusicInfo:
        # songmid
        try:
            # 音乐源地址
            res = _g("https://u.y.qq.com/cgi-bin/musicu.fcg",
                                   data=DEF_MUSIC_QQ_DOWNLOAD_DATA(id),
                                   headers=_MUSIC_QQ_DOWNLOAD_HEADERS)
            res = json.loads(res.text).get("req_0", {}).get("data", {})
            play_list = res.get("midurlinfo", [])

            mp3 = "http://ws.stream.qqmusic.qq.com/"
            if len(play_list) >= 1:
                if play_list[0].get("purl") != "":
                    mp3 +=play_list[0].get("purl", "")
                else:
                    mp3 +=res.get("testfilewifi", "")
            else:
                mp3 +=res.get("testfilewifi", "")
            # 歌词
            _MUSIC_QQ_DOWNLOAD_LYRIC_PARAMS.update({"songmid": id})
            res = re.findall(r'^MusicJsonCallback\((.*?)\)$',
                             _g("http://i.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg",
                                data=_MUSIC_QQ_DOWNLOAD_LYRIC_PARAMS,
                                headers=_MUSIC_QQ_DOWNLOAD_LYRIC_HEADERS).text)[0]
            res = eval(res)
            lrc = base64.b64decode(res.get("lyric")).decode()
            # 基础信息
            body = _g("https://y.qq.com/n/yqq/song/" + id + ".html").text
            _bs = bs4.BeautifulSoup(body, "html.parser")
            imgs = _bs.select(".data__photo")
            img = imgs[0]['src'] if len(imgs) else ""
            song_names = _bs.select(".data__name .data__name_txt")
            song_name = song_names[0].text if len(song_names) else ""
            singers = _bs.select(".data__singer a.data__singer_txt")

            _data = MusicInfo({
                "id": id,
                "name": song_name,
                "mp3_url": mp3,
                "music_url": res.get("data", {}).get("play_backup_url", None),
                "pics": [
                    img,
                ],
                "lyrics": [Lyric({"line": _[1],
                                  "time": _[0]}) for _ in
                           re.findall(r'\[([0-9]{2}:[0-9]{2}.[0-9]*?)\](.*?)\n', lrc)],
                "singers": [Singer({
                    "id": _["data-mid"],
                    "name": _.text,
                    "pics": [
                        img,
                    ]
                }) for _ in singers],
            })
            return ResultMusicInfo(_data)
        except BaseException as base:
            return ResultMusicInfo(None, False)
