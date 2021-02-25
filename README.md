# howard-music
百度、酷狗、酷我、腾讯、网易、咪咕站音乐API

---

## 安装
```console
pip install h_music
```

## 命令行
```console
D:\>h-music

    -v show version
    -s search music
    -p page default `1`
    -d download and lyric (URL)
    -t dataType `json` `format`
    -S Music Source `KG` `BD` `163` `QQ` `KW` `MG`
        `-S` is empty to query all resources. `-p` is invalid.
    -D Download MP3
    示例：alan_walker -S 163
```

## 获取API
```python
from h_music.Site import QQ

qq = QQ()
print(qq.search("薛之谦").to_json())
```