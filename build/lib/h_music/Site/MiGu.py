import json
import re
from ..Empty import Album, Singer, Song, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Empty import ResultSearchMusic, ResultAlbum, ResultMusicInfo
from ..Utils import net_get as _g, net2_session

_MUSIC_MG_SEARCH_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "m.music.migu.cn",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://m.music.migu.cn/v3/search?page=1&type=song&i=eaaabf2729ba6f10feb3b3e92b6533d6888bd832&f=html&s=1607350181&c=001002A&keyword=alan&v=3.13.1",
    "Cookie": "JSESSIONID=58AA28AA568D3768A9BEC26ABC912D2B; mg_uem_user_id_3136357ddb6a49f5b317albumca6254e7ea49=bcb0e0f5-2f27-4408-aec4-e27bcdd22d9a; CookieID=YXCMND17B4XMVVT2EGAX6Z8DECB5VP8Q; migu_cookie_id=46c7fddb-4e41-45d9-8166-b06514409472-n41607335451399; migu_cn_cookie_id=b807a829-435a-4560-81a5-f7b270bf9dc3; Hm_lvt_ec5a5474d9d871cb3d82b846d861979d=1607350078; Hm_lpvt_ec5a5474d9d871cb3d82b846d861979d=1607350112; WT_FPC=id=2bf3b1d890e5436462e1607335273662:lv=1607350182649:ss=1607350065320"
}
_MUSIC_MG_ALL_HEADERS = {
    ":authority": "music.migu.cn",
    ":method": "GET",
    ":path": "/v3/search?page=1&type=song&i=06bb8afd7971a8ef4e8b5128581a9482cd6e9d38&f=html&s=1607352130&c=001002A&keyword=alan&v=3.13.1",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "if-none-match": 'W/"a2f1-GJq8SeSfHs+T2WpvtzSWKjEoEoU',
    "referer": "https://music.migu.cn/v3",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
}


class MiGu(object):
    def __init__(self):
        self.session = net2_session(["https://music.migu.cn/"])

    def search(self, _text, page=1, limit=20) -> ResultSearchMusic:
        try:
            res = _g("https://m.music.migu.cn/migu/remoting/scr_search_tag"
                     "?rows=" + str(limit) + "&type=2&keyword=" + _text + "&pgc=" + str(page),
                     headers=_MUSIC_MG_SEARCH_HEADERS).text
            res = json.loads(res)
            _data = SearchMusic({
                "songs": [Song({
                    "id": _.get("id"),
                    "name": _.get("songName"),
                    "duration": 0,
                    "subtitle": _.get("title", ""),
                    "album": BaseAlbum({
                        "id": _.get("albumId"),
                        "name": _.get("albumName"),
                    }),
                    "singers": [Singer({
                        "id": id,
                        "name": name,
                    }) for id, name in
                        zip(str(_.get("singerId", "")).split(", "), str(_.get("singerName", "")).split(", "))],
                }) for _ in res.get("musics", [])],
                "page": page,
                "limit": limit,
                "songCount": res.get("data", {}).get("total", 0),
            })
            return ResultSearchMusic(_data)
        except BaseException as base:
            return ResultSearchMusic(None, False)

    def album(self, albumid) -> ResultAlbum:
        try:
            # Songs
            res = self.session.get(
                "https://m.music.migu.cn/migu/remoting/cms_album_song_list_tag?albumId=" + albumid + "&pageSize=1000").text
            songs = json.loads(res)
            # Album Info
            res = self.session.get("https://m.music.migu.cn/migu/remoting/cms_album_detail_tag?albumId=" + albumid).text
            res = json.loads(res)
            album = res.get("data", {})
            # Singer Info
            res = self.session.get(
                "https://m.music.migu.cn/migu/remoting/cms_artist_detail_tag?artistId=" + album.get("singerId")).text
            res = json.loads(res)
            singer = res.get("data", {})
            _data = Album({
                "id": albumid,
                "name": album.get("albumName"),
                "publishDate": album.get("publishDate"),
                "description": album.get("albumIntro"),
                "pics": [
                    album.get("albumPicL"),
                    album.get("albumPicM"),
                    album.get("albumPicS"),
                ],
                "singers": [Singer({
                    "id": singer.get("artistId"),
                    "name": singer.get("artistName"),
                    "pics": [
                        singer.get("artistPicL"),
                        singer.get("artistPicM"),
                        singer.get("artistPicS"),
                    ]
                })],
                "songs": [Song({
                    "id": _.get("songId"),
                    "name": _.get("songName"),
                    "duration": 0,
                    "oid": _.get("copyrightId"),
                    "subtitle": _.get("subtitle"),
                    "singers": [Singer({
                        "id": id,
                        "name": name,
                    }) for id, name in zip(_.get("singerId", []), _.get("singerName", []))]
                }) for _ in songs.get("result", {}).get("results", [])],
            })
            return ResultAlbum(_data)
        except BaseException as base:
            return ResultAlbum(None, False)

    def detail(self, id, oid = None) -> ResultMusicInfo:
        try:
            # 获取音乐地址
            res = _g("https://app.c.nf.migu.cn/MIGUM2.0/v2.0/content/listen-url", data={
                "netType": '01',
                "resourceType": 'E',
                "songId": id,
                "toneFlag": {
                    "128": 'PQ',
                    "320": 'HQ',
                    "flac": 'SQ',
                }["320"],
                "dataType": 2,
            }, headers={
                "referer": 'http://music.migu.cn/v3/music/player/audio',
                "channel": '0146951',
                "uid": "1234",
            })
            play = json.loads(res.text)
            lyrics = []
            if oid is not None:
                res = _g("https://m.music.migu.cn/migu/remoting/cms_detail_tag", data={"cpid": oid},
                         headers=_MUSIC_MG_SEARCH_HEADERS)
                res = json.loads(res.text)
                lrc = res.get("data", {}).get("lyricLrc", "")
                lyrics = [Lyric({"line": _[1],
                                      "time": _[0]}) for _ in
                               re.findall(r'\[([0-9]{2}:[0-9]{2}.[0-9]*?)\](.*?)\n', lrc)]
            _data = MusicInfo({
                "id": id,
                "name": play.get("data", {}).get("songItem", {}).get("songName"),
                "mp3_url": play.get("data", {}).get("url", ""),
                "music_url": None,
                "pics": [
                    _.get("img", "") for _ in play.get("data", {}).get("songItem", {}).get("albumImgs", [])
                ],
                "lyrics": lyrics,
                "singers": [Singer({
                    "id": _.get("id"),
                    "name": _.get("name"),
                    "pics": []
                }) for _ in play.get("data", {}).get("songItem", {}).get("artists", [])],
            })
            return ResultMusicInfo(_data)
        except BaseException as base:
            return ResultMusicInfo(None, False)
