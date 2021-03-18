# howard-music

百度、酷狗、酷我、腾讯、网易、咪咕 API

![GitHub branch checks state](https://img.shields.io/github/checks-status/tt20050510/howard-music/main)

> 项目仅供学习参考，请勿商用！
---

## 安装

```console
pip install h-music
```

## 命令行**

```console
D:\>h-music --help
+-------------------------------+-------------------------------+----------------------------------------+
| option                        | use                           | arg                                    |
+-------------------------------+-------------------------------+----------------------------------------+
| -v --version                  |                               | 查看版本信息                           |
| -h --help                     |                               | 查看帮助文本                           |
| -s --search=<text>            | h-music -s xxx or h-music xxx | 搜索文本(选用)                         |
| -p --page=<number>            | h-music -s xxx -S 163 page 1  | 搜索分页                               |
|                               |                               | (需要配合--source使用)                 |
| -d --detail=<id>              | h-music -d <id>               | 查看详细信息                           |
|                               |                               | (包含艺术家、歌曲名称、歌词、源地址)   |
| -a --album=<id>               | h-music -a <id>               | 查看专辑详细信息(仅支持json格式)       |
| -t --type=<`json`,`table`>    | h-music xxx -t json           | 输出格式，支持`json`和`table`          |
| -S --source=<source>          | h-music xxx -s 163            | 搜索源(`kg`,`bd`,`163`,`qq`,`kw`,`mg`) |
| -D --download                 | h-music -d <id> -D            | 保存源文件，在--detail时生效           |
| -P --download_path=<dir_path> | h-music -d <id> -D -P D:      | 源文件保存路径                         |
|                               |                               | (它可以包含--download但必须有参数)     |
|                               |                               | 示例：h-music alan_walker -S 163       |
+-------------------------------+-------------------------------+----------------------------------------+
```

## 获取API

更多功能请参阅[详细API](https://book.ipyhub.top/yin-le-zhan-shu-ju-api/yin-le-zhan-apipython)

```python
from h_music.Site import QQ

qq = QQ()
print(qq.search("薛之谦").to_json())
```

``` shell
█████████████████████████████████████████████
█████████████████████████████████████████████
████ ▄▄▄▄▄ ██ █▄██▄  █▄▄ ██▄ ▀▄▀▄█ ▄▄▄▄▄ ████
████ █   █ █  ▄ ▄ ██▀▀█▀▄▄▄ ▀▀▄█▀█ █   █ ████
████ █▄▄▄█ █ ▄ █▀██▀▄▀▀▄▄▀▀▄██ ▀██ █▄▄▄█ ████
████▄▄▄▄▄▄▄█ ▀▄▀▄█▄▀▄█▄█ ▀ ▀▄█ ▀ █▄▄▄▄▄▄▄████
████ ▀  ▄▄▄██▀ █▀   ▀▄▀▀██▄ ▄ █▄▀█▄ ▄▄ ▀█████
████  █▀▀ ▄▀▀██▄████▀▄ ▀▀▀▄█▀██  ▄ ▄███▄ ████
████▀▄▀▀ ▀▄▄▄▀█▄▄ ▀█ ▄▀ ▀█▄ ▄ ██▄▀▄▄▄▄▄▄▄████
████▄▀▀  ▀▄ █  █ ▄ ▄ █▄█▄ ▄▀██ ▄▄▄█  ▄██▄████
████ ▄▄▀▄█▄▄▄▀▀█▀▀▄▀█ ▀ ▀█▄ ▄ ▄▄██▄▀▄█  █████
████▄▄█▄▄ ▄▀ █ ▀ ▄   ▄▀█▄ ▀█▀▄▄  ▀▄█▀▄█▄ ████
████   █▄▄▄ ▄▄ ▀▄█▄▄█ ▀▀▀▀▄ ▄▄▄▄▄▀▄█▄ ▄██████
████▀▄▀▄ ▀▄██████▀▀▄▄▄▀██  ▀ █▀ █ ▀  ▄█  ████
████ ▀█▄ ▄▄█▀▄▄█▄█▄▄  ▀▀▀██▀█▄ █  ▄▀▄█▄██████
████ █  ▄▀▄█ ▀▄ ▀ ▀▄▄▄███▀ ▀█▄  █ ▄█ ▀█ ▄████
████▄███▄█▄█▀█▄▄▀▀ █ ▄█  ██ ▄▄▄█ ▄▄▄  ▄█▄████
████ ▄▄▄▄▄ █▀▄▀ ▀ █  ▄█▀▄  █▄██▀ █▄█ ▀▄  ████
████ █   █ █ ▄▀ ▀▄█▄▀▄ ▀▀█ ▀  ▄▄▄▄ ▄ █ ▀▀████
████ █▄▄▄█ █▄▀ ▄▄▄▀  █▀▀█▀ █▀█▀  ▄▀█▀██▄ ████
████▄▄▄▄▄▄▄█▄▄██▄▄▄██▄█▄▄█▄▄█▄▄██▄██▄█▄▄▄████
█████████████████████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

## 源支持
> 目前支持以下来源，均支持API操作，部分支持命令操作。

|  来源   | 代码  |  音乐源文件   |  封面   |  歌词   |  收费   |  专辑   | 分页  |
|  :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  |
| 网易  | 163 |✓|✓|✓|×|✓|✓|
| 腾讯  | qq |✓|✓|✓|×|✓|✓|
| 酷狗  | kg |✓|✓|✓|×|✓|✓|
| 酷我  | kw |✓|✓|✓|×|✓|✓|
| 咪咕  | mg |✓|✓|✓|×|✓|✓|
| 千千  | bd |✓|✓|✓|×|✓|×|

## 问题
项目具有实验性，出现故障时请移步[issues](/issues)寻求解决
> 若非Python环境，请移步[releases](/releases)，下载可执行版本。

## 作者留言
仓库开源供学习使用，感兴趣者请Star支持作者，谢谢。
