import getopt
import json
import os
import sys
import base64
from typing import Dict, Any
from .Utils import prettytable as pt, _STR_TO_FILE_NAME_
from .Utils import net_get as _g
from .Site import KuGou, QQ, QianQian, KuWo, NetEase, MiGu

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


def printFormat(datas, _TYPE, count=0, page=1):
    if _TYPE == "json":
        print(json.dumps({
            "count": count,
            "datas": [{
                "id": id_decode(_),
                "info": _
            } for _ in datas]
        }, ensure_ascii=True))
    elif _TYPE == "table":
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


def printFormatDetail(data, _TYPE):
    if _TYPE == "json":
        print(json.dumps(data, ensure_ascii=True))
    elif _TYPE == "table":
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


def printFormatError(_TYPE):
    if _TYPE == "json":
        print(json.dumps({
            "code": 0
        }, ensure_ascii=True))
    elif _TYPE == "table":
        tb = pt.PrettyTable()
        tb.field_names = ["错误"]
        tb.add_row(["无法获取"])
        print(tb)

def out_version():
    tb = pt.PrettyTable()
    tb.field_names = ["version", "h_music. 0.1.4"]
    tb.add_row(["******", "ipyhub.top"])
    tb.add_row(["              ", "请勿商用"])
    print(tb)

def main(**kwargs):
    dataType = ["json", "table"]
    _TYPE = "table"
    _SEARCH = None
    _CUR_CODE = None
    _SOURCE_CLS = None
    _SOURCE_CLS_NAME = None
    _VERSION = False
    _DETAIL = False
    _DETAIL_TEXT = None
    _PAGE = 1
    _DOWNLOAD = False
    _DOWNLOAD_PATH = os.path.expanduser('~') + "\\Music\\"
    _MUSIC_DATA = None
    _ALBUM = None
    argv = sys.argv[1:]
    _HELP_TEXT = pt.PrettyTable()
    _HELP_TEXT.field_names = ["option", "use", "arg"]
    _HELP_TEXT.add_row(["-v --version","", "查看版本信息"])
    _HELP_TEXT.add_row(["-h --help","", "查看帮助文本"])
    _HELP_TEXT.add_row(["-s --search=<text>","h-music -s xxx or h-music xxx", "搜索文本(选用)"])
    _HELP_TEXT.add_row(["-p --page=<number>","h-music -s xxx -S 163 page 1", "搜索分页\n(需要配合--source使用)"])
    _HELP_TEXT.add_row(["-d --detail=<id>","h-music -d <id>", "查看详细信息\n(包含艺术家、歌曲名称、歌词、源地址)"])
    _HELP_TEXT.add_row(["-a --album=<id>","h-music -a <id>", "查看专辑详细信息(仅支持json格式)"])
    _HELP_TEXT.add_row(["-t --type=<`json`,`table`>","h-music xxx -t json", "输出格式，支持`json`和`table`"])
    _HELP_TEXT.add_row(["-S --source=<source>","h-music xxx -s 163", "搜索源(`kg`,`bd`,`163`,`qq`,`kw`,`mg`)"])
    _HELP_TEXT.add_row(["-D --download","h-music -d <id> -D", "保存源文件，在--detail时生效"])
    _HELP_TEXT.add_row(["-P --download_path=<dir_path>","h-music -d <id> -D -P D:", "源文件保存路径\n(它可以包含--download但必须有参数)"])
    _HELP_TEXT.add_row(["","","示例：h-music alan_walker -S 163"])
    _HELP_TEXT.valign = "m"
    _HELP_TEXT.align = "l"

    #######################################
    len_code = len(argv)

    if len_code == 0 or (len_code == 1 and argv[0] in ['-h','--help']):
        print(_HELP_TEXT)
        sys.exit(0)
    else:
        if not argv[0] in "-s:-v:-a:-d:-S:-t:-D:-p:-P:-h:--help:--version:--text:--album:--detail:--source:--type:--download_path:--download:--page".split(":"):
            _SEARCH = argv[0].replace("_", "")
            del argv[0]
        elif argv[0] in "-v:--version".split(":"):
            out_version()
            sys.exit(0)
    #######################################
    try:
        opts, args = getopt.getopt(argv, "-s:-v-a:-d:-S:-t:-P:-D-p:-h:",
                                   ["text", "version", "album=", "detail=", "source=", "type=", "download_path",
                                    "download", "page",
                                    "help"])
    except getopt.GetoptError:
        print(_HELP_TEXT)
        sys.exit(2)
    #######################################
    for opt, arg in opts:
        if opt in ("-v", "--version"):
            out_version()
            sys.exit(0)
        elif opt in ("-s", "--text"):
            _SEARCH = arg.replace("_", "")
        elif opt in ("-p", "--page"):
            try:
                _PAGE = int(arg)
            except:
                print("`%s` is the wrong number type" % arg)
        elif opt in ("-t", "--type"):
            if not arg in dataType:
                print("data type '%s' does not exist" % arg)
                sys.exit(0)
            _TYPE = arg
        elif opt in ("-S", "--Source"):
            if _DETAIL:
                print("command cannot be used at the same time.")
                sys.exit(0)
            arg = arg.lower()
            if not arg in source.keys():
                print("source '%s' does not exist" % arg)
                sys.exit(0)
            _SOURCE_CLS = source.get(arg)
            _SOURCE_CLS_NAME = arg
        elif opt in ("-d", "--detail"):
            if _SEARCH:
                print("command cannot be used at the same time.")
                sys.exit(0)
            _DETAIL = True
            _DETAIL_TEXT = arg
        elif opt in ("-a", "--album"):
            _ALBUM = True
            _DETAIL_TEXT = arg
        elif opt in ("-D", "--download"):
            _DOWNLOAD = True
        elif opt in ("-P", "--download_path"):
            _DOWNLOAD = True
            if os.path.isdir(arg):
                _DOWNLOAD_PATH = arg
            else:
                print("path `%s` does not exist" % arg)
                sys.exit(0)
        else:
            print("command '%s' does not exist" % opt)
            sys.exit(0)

    if _SEARCH is not None:
        data = []
        if _SOURCE_CLS is not None:
            res = _SOURCE_CLS.search(_SEARCH, _PAGE)
            if res.state:
                for _ in res.data.to_dict().get("songs"):
                    _.update({"source": _SOURCE_CLS_NAME})
                    data.append(_)
                printFormat(data, _TYPE, res.data.songCount, res.data.page)
            else:
                printFormatError(_TYPE)

        else:
            for key, rs in source.items():
                res = rs.search(_SEARCH)
                if res.state:
                    for _ in res.data.to_dict().get("songs"):
                        _.update({"source": key})
                        data.append(_)
                else:
                    printFormatError(_TYPE)
            printFormat(data, _TYPE)


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
                printFormatDetail(res.data.to_dict(), _TYPE)
                _MUSIC_DATA = res.data.to_dict()
            else:
                printFormatError(_TYPE)
        else:
            print("Parsing error!")
            sys.exit(0)
    if _DOWNLOAD:
        if _MUSIC_DATA is not None:
            mp3_url = _MUSIC_DATA.get("mp3_url")
            if mp3_url is not None and not mp3_url[:4] == "http":
                mp3_url = "http://" + mp3_url
            content = _g(mp3_url).content
            _FILE_NAME = " ".join(
                [_MUSIC_DATA.get("name"), "-", "&".join([_.get("name") for _ in _MUSIC_DATA.get("singers", [])])])
            _FILE_NAME = _STR_TO_FILE_NAME_(_FILE_NAME)
            _SAVE_FILE_PATH = os.path.join(_DOWNLOAD_PATH, _FILE_NAME + ".mp3")
            with open(_SAVE_FILE_PATH, mode="wb") as wb:
                wb.write(content)
            print("Download -> " + _SAVE_FILE_PATH)
        else:
            print("Need the support of '-d'")
            print("as -d xxx -D")

    if _ALBUM:
        if (_DETAIL_TEXT):
            ss = id_encode(_DETAIL_TEXT)
            m = source.get(ss[1], None)
            if m is not None:
                print(json.dumps(m.album(ss[2]).to_dict(), ensure_ascii=True))
            else:
                print("Parsing error!")
                sys.exit(0)
        else:
            print("`DETAIL ID` not received")


if __name__ == '__main__':
    main()
