# howard-music
百度、酷狗、酷我、腾讯、网易、咪咕 API

---

## 安装
```console
pip install h-music
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
更多功能请参阅[详细API](https://437983438.gitbook.io/spidernotes/yin-le-zhan-shu-ju-api/yin-le-zhan-apipython)
```python
from h_music.Site import QQ

qq = QQ()
print(qq.search("薛之谦").to_json())
```
> 输出结果
```json
{
  "state": true,
  "data": {
    "songs": [
      {
        "id": "0013WPvt4fQH2b",
        "name": "天外来物",
        "subtitle": "天外来物",
        "duration": 257,
        "album": {
          "id": "000K9Zp13TZp5s",
          "name": "天外来物"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001WHzlF1VWXiR",
        "name": "动物世界 (Live)",
        "subtitle": "动物世界 (Live)",
        "duration": 0,
        "album": {
          "id": "",
          "name": ""
        },
        "privilege": false,
        "singers": [
          {
            "id": "001IoTZp19YMDG",
            "name": "易烊千玺",
            "pics": []
          },
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "000K74Op0OV8Cm",
        "name": "演员",
        "subtitle": "演员",
        "duration": 261,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "002BWGZQ2UKjKn",
        "name": "你还要我怎样",
        "subtitle": "你还要我怎样",
        "duration": 310,
        "album": {
          "id": "000QgFcm0v8WaF",
          "name": "意外"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001ndJe947wlaP",
        "name": "绅士",
        "subtitle": "绅士",
        "duration": 290,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001TXSYu1Gwuwv",
        "name": "刚刚好",
        "subtitle": "刚刚好",
        "duration": 250,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "004VBMk71TdUuR",
        "name": "我好像在哪见过你",
        "subtitle": "我好像在哪见过你",
        "duration": 279,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "004dADLe4ec8RG",
        "name": "意外",
        "subtitle": "意外",
        "duration": 287,
        "album": {
          "id": "000QgFcm0v8WaF",
          "name": "意外"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "000BZ9Fg16MAU2",
        "name": "耗尽",
        "subtitle": "耗尽",
        "duration": 259,
        "album": {
          "id": "000K9Zp13TZp5s",
          "name": "天外来物"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          },
          {
            "id": "002Jhik52k49N3",
            "name": "郭聪明",
            "pics": []
          }
        ]
      },
      {
        "id": "003v4UL61IYlTY",
        "name": "暧昧",
        "subtitle": "暧昧",
        "duration": 312,
        "album": {
          "id": "001L7UIu3GXVtT",
          "name": "渡 The Crossing"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "003FFWnA3AIczD",
        "name": "怪咖",
        "subtitle": "怪咖",
        "duration": 250,
        "album": {
          "id": "0015rUVB2OUdGA",
          "name": "怪咖"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001hUNRP0P8g7x",
        "name": "认真的雪",
        "subtitle": "认真的雪",
        "duration": 261,
        "album": {
          "id": "003mUYW22JXKVK",
          "name": "薛之谦"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001uxKNp3a7Qkv",
        "name": "像风一样",
        "subtitle": "像风一样",
        "duration": 255,
        "album": {
          "id": "001L7UIu3GXVtT",
          "name": "渡 The Crossing"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001RlxZp1xwoNK",
        "name": "方圆几里",
        "subtitle": "方圆几里",
        "duration": 263,
        "album": {
          "id": "000QgFcm0v8WaF",
          "name": "意外"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "003ouHMP12glVD",
        "name": "其实",
        "subtitle": "其实",
        "duration": 242,
        "album": {
          "id": "000QgFcm0v8WaF",
          "name": "意外"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "002JPGWQ3ivuVZ",
        "name": "一半",
        "subtitle": "一半",
        "duration": 286,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "000QwTVo0YHdcP",
        "name": "丑八怪",
        "subtitle": "丑八怪",
        "duration": 248,
        "album": {
          "id": "000QgFcm0v8WaF",
          "name": "意外"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "001KhneD0yEIzz",
        "name": "下雨了",
        "subtitle": "下雨了",
        "duration": 305,
        "album": {
          "id": "000dcZ9I1nzO62",
          "name": "初学者"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "002lSUhO4Z4J1o",
        "name": "天后 (Live)",
        "subtitle": "天后 (Live)",
        "duration": 247,
        "album": {
          "id": "001mH3KE1Z6Prd",
          "name": "蒙面唱将猜猜猜第二季 第11期"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      },
      {
        "id": "003RCA7t0y6du5",
        "name": "动物世界",
        "subtitle": "动物世界",
        "duration": 230,
        "album": {
          "id": "001L7UIu3GXVtT",
          "name": "渡 The Crossing"
        },
        "privilege": false,
        "singers": [
          {
            "id": "002J4UUk29y8BY",
            "name": "薛之谦",
            "pics": []
          }
        ]
      }
    ],
    "page": 1,
    "limit": 20,
    "songCount": 150
  }
}
```

