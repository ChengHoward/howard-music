import base64
import binascii
import json
import os
import re
import time
import bs4
from Crypto.Cipher import AES

from ..Empty import Album, Singer, Song, BaseAlbum, SearchMusic, MusicInfo, Lyric
from ..Empty import ResultSearchMusic, ResultAlbum, ResultMusicInfo
from ..Utils.request import net_get as _g, net_post as _p, net2_session


class NetEase(object):
    def __init__(self):
        self.session = net2_session(["http://m.kugou.com/", "https://m3ws.kugou.com/"])

    def _create_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]

    def _aes(self, text, key):
        pad = 16 - len(text) % 16
        text = text + bytearray([pad] * pad)
        encryptor = AES.new(key, 2, b"0102030405060708")
        ciphertext = encryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    def _rsa(self, text, pubkey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
        return format(rs, "x").zfill(256)

    def _encrypted_request(self, data) -> dict:
        MODULUS = (
            "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7"
            "b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280"
            "104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932"
            "575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b"
            "3ece0462db0a22b8e7"
        )
        PUBKEY = "010001"
        NONCE = b"0CoJUm6Qyw8W8jud"
        data = json.dumps(data).encode("utf-8")
        secret = self._create_key(16)
        params = self._aes(self._aes(data, NONCE), secret)
        encseckey = self._rsa(secret, PUBKEY, MODULUS)
        return {"params": params, "encSecKey": encseckey}

    def search(self, _text, page=1, limit=20) -> ResultSearchMusic:
        try:
            res = json.loads(_p("http://music.163.com/api/search/pc", data={
                'limit': limit,
                'offset': (page - 1) * limit,
                's': _text,
                'type': 1,
            }).text)
            _data = SearchMusic({
                "songs": [Song({
                    "id": _.get("id"),
                    "name": _.get("name"),
                    "duration": int(_.get("duration", 0) / 1000),
                    "subtitle": None,
                    "privilege": not (_.get("privilege", {}).get("fl", 0) == 0),
                    "album": BaseAlbum({
                        "id": _.get("album", {}).get("id"),
                        "name": _.get("album", {}).get("name"),
                    }),
                    "singers": [Singer({
                        "id": __.get("id"),
                        "name": __.get("name"),
                    }) for __ in _.get("artists", [])],
                }) for _ in res.get("result", {}).get("songs")],
                "page": page,
                "limit": limit,
                "songCount": res.get("result", {}).get("songCount")
            })
            return ResultSearchMusic(_data)
        except:
            return ResultSearchMusic(None, False)

    def album(self, albumid) -> ResultAlbum:
        try:
            res = _p("https://interface.music.163.com/weapi/v1/album/" + albumid, data=self._encrypted_request({}))
            res = json.loads(res.text)
            album = res.get("album", {})
            songs = [{
                "songid": _.get("id"),
                "songname": _.get("name"),
                "subtitle": _.get("name"),
            } for _ in res.get("songs")]
            _data = Album({
                "id": albumid,
                "name": album.get("name"),
                "publishDate": time.strftime("%Y-%m-%d", time.localtime(album.get("publishTime", 0) / 1000.0)),
                "description": album.get("description"),
                "pics": [
                    album.get("picUrl"),
                    album.get("blurPicUrl"),
                ],
                "singers": [Singer({
                    "id": __.get("id"),
                    "name": __.get("name"),
                }) for __ in album.get("artists", [])],
                "songs": [Song({
                    "id": _.get("id"),
                    "name": _.get("name"),
                    "subtitle": None,
                    "duration": _.get("Duration", 0),
                    "singers": [Singer({
                        "id": __.get("id"),
                        "name": __.get("name"),
                    }) for __ in _.get("ar", [])]
                }) for _ in res.get("songs")],
            })
            return ResultAlbum(_data)
        except:
            return ResultAlbum(None, False)

    def detail(self, id) -> ResultMusicInfo:
        try:
            # Play URL
            res = _p("http://music.163.com/weapi/song/enhance/player/url", data=self._encrypted_request({
                "ids": [id, ],
                "br": 32000
            }))
            play = json.loads(res.text).get("data")[0]
            # Lyric
            lrc = _p("https://music.163.com/weapi/song/lyric",
                     data=self._encrypted_request({"csrf_token": "", "id": id, "lv": -1, "tv": -1}))
            lrc = json.loads(lrc.text).get("lrc", {}).get("lyric", "")
            # INFO
            body = _g("https://music.163.com/song?id=" + id).text
            _bs = bs4.BeautifulSoup(body, "html.parser")
            imgs = _bs.select(".j-img")
            img = imgs[0]['src'] if len(imgs) else ""
            song_names = _bs.select(".tit .f-ff2")
            song_name = song_names[0].text if len(song_names) else ""
            singers = _bs.select(".des span .s-fc7")
            _data = MusicInfo({
                "id": play.get("id"),
                "name": song_name,
                "mp3_url": play.get("url", ""),
                "music_url": None,
                "pics": [
                    img,
                ],
                "lyrics": [Lyric({"line": _[1],
                                  "time": _[0]}) for _ in
                           re.findall(r'\[([0-9]{2}:[0-9]{2}.[0-9]*?)\](.*?)\n', lrc)],
                "singers": [Singer({
                    "id": str(_["href"]).replace("/artist?id=",""),
                    "name": _.text,
                    "pics": [
                        img,
                    ]
                }) for _ in singers]
            })
            return ResultMusicInfo(_data)
        except:
            return ResultMusicInfo(None, False)
