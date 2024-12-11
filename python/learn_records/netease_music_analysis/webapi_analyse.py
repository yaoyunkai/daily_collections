"""
document for netease_webapi_analyse.py


function a(a) {
    var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
    for (d = 0; a > d; d += 1)
        e = Math.random() * b.length,
        e = Math.floor(e),
        c += b.charAt(e);
    return c
}
function b(a, b) {
    var c = CryptoJS.enc.Utf8.parse(b)
      , d = CryptoJS.enc.Utf8.parse("0102030405060708")
      , e = CryptoJS.enc.Utf8.parse(a)
      , f = CryptoJS.AES.encrypt(e, c, {
        iv: d,
        mode: CryptoJS.mode.CBC
    });
    return f.toString()
}
function c(a, b, c) {
    var d, e;
    return setMaxDigits(131),
    d = new RSAKeyPair(b,"",c),
    e = encryptedString(d, a)
}
function d(d, e, f, g) {
    var h = {}
      , i = a(16);
    return h.encText = b(d, g),
    h.encText = b(h.encText, i),
    h.encSecKey = c(i, e, f),
    h
}
function e(a, b, d, e) {
    var f = {};
    return f.encText = c(a + e, b, d),
    f
}
window.asrsea = d,
window.ecnonasr = e


created at 2024/9/11 14:39
"""
import json
from base64 import b64encode

import requests
from Crypto.Cipher import AES

req_data = {
    "rid": "R_SO_4_27867449",
    "threadId": "R_SO_4_27867449",
    "pageNo": "1",
    "pageSize": "20",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "csrf_token": ""
}

url_path = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

data1 = {
    'emj': {
        "色": "00e0b",
        "流感": "509f6",
        "这边": "259df",
        "弱": "8642d",
        "嘴唇": "bc356",
        "亲": "62901",
        "开心": "477df",
        "呲牙": "22677",
        "憨笑": "ec152",
        "猫": "b5ff6",
        "皱眉": "8ace6",
        "幽灵": "15bb7",
        "蛋糕": "b7251",
        "发怒": "52b3a",
        "大哭": "b17a8",
        "兔子": "76aea",
        "星星": "8a5aa",
        "钟情": "76d2e",
        "牵手": "41762",
        "公鸡": "9ec4e",
        "爱意": "e341f",
        "禁止": "56135",
        "狗": "fccf6",
        "亲亲": "95280",
        "叉": "104e0",
        "礼物": "312ec",
        "晕": "bda92",
        "呆": "557c9",
        "生病": "38701",
        "钻石": "14af6",
        "拜": "c9d05",
        "怒": "c4f7f",
        "示爱": "0c368",
        "汗": "5b7a4",
        "小鸡": "6bee2",
        "痛苦": "55932",
        "撇嘴": "575cc",
        "惶恐": "e10b4",
        "口罩": "24d81",
        "吐舌": "3cfe4",
        "心碎": "875d3",
        "生气": "e8204",
        "可爱": "7b97d",
        "鬼脸": "def52",
        "跳舞": "741d5",
        "男孩": "46b8e",
        "奸笑": "289dc",
        "猪": "6935b",
        "圈": "3ece0",
        "便便": "462db",
        "外星": "0a22b",
        "圣诞": "8e7",
        "流泪": "01000",
        "强": "1",
        "爱心": "0CoJU",
        "女孩": "m6Qyw",
        "惊恐": "8W8ju",
        "大笑": "d"
    },
    'md': [
        "色",
        "流感",
        "这边",
        "弱",
        "嘴唇",
        "亲",
        "开心",
        "呲牙",
        "憨笑",
        "猫",
        "皱眉",
        "幽灵",
        "蛋糕",
        "发怒",
        "大哭",
        "兔子",
        "星星",
        "钟情",
        "牵手",
        "公鸡",
        "爱意",
        "禁止",
        "狗",
        "亲亲",
        "叉",
        "礼物",
        "晕",
        "呆",
        "生病",
        "钻石",
        "拜",
        "怒",
        "示爱",
        "汗",
        "小鸡",
        "痛苦",
        "撇嘴",
        "惶恐",
        "口罩",
        "吐舌",
        "心碎",
        "生气",
        "可爱",
        "鬼脸",
        "跳舞",
        "男孩",
        "奸笑",
        "猪",
        "圈",
        "便便",
        "外星",
        "圣诞"
    ]
}

# 服务于d的
f = ("00e0b509f6259df8642dbc35662901477df22677ec152b5ff68"
     "ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341"
     "f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f"
     "0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef"
     "52741d546b8e289dc6935b3ece0462db0a22b8e7")
g = "0CoJUm6Qyw8W8jud"
e = "010001"
i = "d5bpgMn9byrHNtAh"  # 手动固定的. -> 人家函数中是随机的


def get_encSecKey():  # 由于i是固定的. 那么encSecText就是固定的.  c()函数的结果就是固定的
    return ("1b5c4ad466aabcfb713940efed0c99a1030bce2456462c73d8383c60e751b069c"
            "24f82e60386186d4413e9d7f7a9c7cf89fb06e40e52f28b84b8786b476738a12b81"
            "ac60a3ff70e00b085c886a6600c012b61dbf418af84eb0be5b735988addafbd7221"
            "903c44d027b2696f1cd50c49917e515398bcc6080233c71142d226ebb")


# 把参数进行加密
def get_params(data):  # 默认这里接收到的是字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second  # 返回的就是params


# 转化成16的倍数, 为下方的加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


# 加密过程
def enc_params(data, key):
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密, 加密的内容的长度必须是16的倍数
    return str(b64encode(bs), "utf-8")  # 转化成字符串返回,


resp = requests.post(url_path, data={
    "params": get_params(json.dumps(req_data)),
    "encSecKey": get_encSecKey()
})

print(resp.content.decode('utf8'))
