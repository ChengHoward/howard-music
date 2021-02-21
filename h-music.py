import json
import os
import sys
import base64
import re
from typing import Dict, Any
from Utils import prettytable as pt, _STR_TO_FILE_NAME_
from Utils import net_get as _g
from Site import KuGou, QQ, QianQian, KuWo, NetEase, MiGu
import urllib

_SAVE_PATH = "C:\\Users\\Howard\\Desktop\\"

argv = sys.argv
_HELP_TEXT = """
    -v show version
    -s search music
    -p page default `1`
    -d download(URL) and lyric 
    -a album only `json` data
    -t dataType `json` `format`
    -S Music Source `KG` `BD` `163` `QQ` `KW` `MG`
        `-S` is empty to query all resources. `-p` is invalid.
    -D Download MP3
    示例：alan_walker -S 163
    """
#######################################
len_code = len(argv)
if len_code == 1:
    print(_HELP_TEXT)
    sys.exit(0)

code = {
    "v": "version",
    "s": "search",
    "S": "source",
    "d": "detail",
    "a": "album",
    "t": "type",
    "p": "page",
    "D": "download",
}
source: Dict[str, Any] = {
    "kg": KuGou(),
    "bd": QianQian(),
    "163": NetEase(),
    "qq": QQ(),
    "kw": KuWo(),
    "mg": MiGu(),
}
dataType = ["json", "format"]
_TYPE = "format"
_SEARCH = None
_CUR_CODE = None
_SOURCE_CLS = None
_SOURCE_CLS_NAME = None
_VERSION = False
_DETAIL = False
_DETAIL_TEXT = None
_PAGE = 1
_DOWNLOAD = False
_DOWNLOAD_PATH = os.path.expanduser('~')+"\\Music\\"
_MUSIC_DATA = None
_ALBUM = None
i = 0
# 命令解析
for _ in argv[1:]:
    if _CUR_CODE:
        if _CUR_CODE == "search":
            _SEARCH = _.replace("_", "")
        if _CUR_CODE == "page":
            try:
                _PAGE = int(_)
            except:
                print("`%s` is the wrong number type" % _)
        if _CUR_CODE == "type":
            if not _ in dataType:
                print("data type '%s' does not exist" % _)
                sys.exit(0)
            _TYPE = _
        elif _CUR_CODE == "source":
            _ = _.lower()
            if not _ in source.keys():
                print("source '%s' does not exist" % _)
                sys.exit(0)
            _SOURCE_CLS = source.get(_)
            _SOURCE_CLS_NAME = _
        elif _CUR_CODE == "detail":
            _DETAIL = True
            _DETAIL_TEXT = _
        elif _CUR_CODE == "album":
            _DETAIL_TEXT = _
        elif _CUR_CODE == "download":
            try:
                _DOWNLOAD_PATH = _
            except:
                print("`%s` is the wrong number type" % _)
        _CUR_CODE = None
    else:
        _c = re.findall(r'^-(.*?)$', _)
        if len(_c) > 0:
            _c = code.get(_c[0])
        if _c == "search":
            _CUR_CODE = _c
        elif _c == "type":
            _CUR_CODE = _c
        elif _c == "source":
            _CUR_CODE = _c
        elif _c == "detail":
            _CUR_CODE = _c
        elif _c == "page":
            _CUR_CODE = _c
        elif _c == "download":
            _DOWNLOAD = True
        elif _c == "album":
            _CUR_CODE = _c
            _ALBUM = True
        elif _c == "version":
            tb = pt.PrettyTable()
            tb.field_names = ["version", "h-music. 20201213"]
            tb.add_row(["******", "Howardyun.top"])
            tb.add_row(["              ", "请勿商用"])
            print(tb)
            sys.exit(0)
        else:
            if i == 0:
                _SEARCH = _
            else:
                print("command '%s' does not exist" % _)
                sys.exit(0)
    i += 1


def id_decode(text):
    return base64.b64encode("|".join([str(text.get("id")),
                                      str(text.get("source")),
                                      str(text.get("album").get("id")),
                                      str(text.get("oid", ""))]).encode()).decode()


def id_encode(text):
    try:
        return (base64.b64decode(text).decode()).split("|")
    except:
        return []


def printFormat(datas, count=0, page=1):
    if _TYPE == "json":
        print(json.dumps({
            "count": count,
            "datas": [{
                "id":id_decode(_),
                "info":_
            } for _ in datas]
        },ensure_ascii=True))
    elif _TYPE == "format":
        tb = pt.PrettyTable()
        tb.field_names = ["名称", "歌手", "时长", "id", "来源"]
        for _ in datas:
            tb.add_row([_.get("name"),
                        "/".join([__.get("name") for __ in _.get("singers")]),
                        _.get("duration"),
                        id_decode(_),
                        _.get("source")])
        if not count == 0:
            limit = len(datas)
            tb.add_row(["", "", "", "", ""])
            tb.add_row(["", "", "", "总量：%s" % count,
                        "%s/%s" % (str(page), str((count // limit) + (1 if count % limit > 0 else 0)))])
        print(tb)


def printFormatDetail(data):
    if _TYPE == "json":
        print(json.dumps(data,ensure_ascii=True))
    elif _TYPE == "format":
        tb = pt.PrettyTable()
        tb.title = "详细信息"
        tb.field_names = ["歌曲名", data.get("name")]
        tb.add_row(["歌手", "/".join([_.get("name") for _ in data.get("singers", [])])])
        print(tb)
        tb = pt.PrettyTable()
        tb.field_names = ["Time", "歌词"]
        for _ in data.get("lyrics"):
            tb.add_row([_.get("time"), str(_.get("line")).replace(" ", "").replace("\r", "")])
        print(tb)
        tb = pt.PrettyTable()
        tb.field_names = ["源地址"]
        tb.add_row([data.get("mp3_url")])
        print(tb)


def printFormatError():
    if _TYPE == "json":
        print(json.dumps({
            "code": 0
        },ensure_ascii=True))
    elif _TYPE == "format":
        tb = pt.PrettyTable()
        tb.field_names = ["错误"]
        tb.add_row(["无法获取"])
        print(tb)


if _SEARCH is not None:
    data = []
    if _SOURCE_CLS is not None:
        res = _SOURCE_CLS.search(_SEARCH, _PAGE)
        if res.state:
            for _ in res.data.to_dict().get("songs"):
                _.update({"source": _SOURCE_CLS_NAME})
                data.append(_)
            printFormat(data, res.data.songCount, res.data.page)
        else:
            printFormatError()

    else:
        for key, rs in source.items():
            res = rs.search(_SEARCH)
            if res.state:
                for _ in res.data.to_dict().get("songs"):
                    _.update({"source": key})
                    data.append(_)
            else:
                printFormatError()
        printFormat(data)


elif _DETAIL and _DETAIL is not None:
    ss = id_encode(_DETAIL_TEXT)
    m = source.get(ss[1], None)
    if m is not None:
        if ss[1] in ["bd", "163", "qq", "kw"]:
            res = m.detail(ss[0])
        elif ss[1] in ["kg"]:
            res = m.detail(ss[0], ss[2])
        elif ss[1] in ["mg"]:
            res = m.detail(ss[0], ss[3])
        if res.state:
            printFormatDetail(res.data.to_dict())
            _MUSIC_DATA = res.data.to_dict()
        else:
            printFormatError()
    else:
        print("Parsing error!")
        sys.exit(0)
if _DOWNLOAD:
    if _MUSIC_DATA is not None:
        content = _g(_MUSIC_DATA.get("mp3_url")).content
        _FILE_NAME = " ".join([_MUSIC_DATA.get("name"),"-","&".join([_.get("name") for _ in _MUSIC_DATA.get("singers", [])])])
        _FILE_NAME = _STR_TO_FILE_NAME_(_FILE_NAME)
        with open(_DOWNLOAD_PATH+_FILE_NAME+".mp3",mode="wb") as wb:
            wb.write(content)
        print("Download -> " + _DOWNLOAD_PATH+_FILE_NAME+".mp3")
    else:
        print("Need the support of '-d'")
        print("as -d xxx -D")


if _ALBUM:
    if (_DETAIL_TEXT):
        ss = id_encode(_DETAIL_TEXT)
        m = source.get(ss[1], None)
        if m is not None:
            print(json.dumps(m.album(ss[2]).to_dict(),ensure_ascii=True))
        else:
            print("Parsing error!")
            sys.exit(0)
    else:
        print("`DETAIL ID` not received")
