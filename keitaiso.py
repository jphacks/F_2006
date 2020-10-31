# 受け取った文章を形態素解析して返す
# 型は辞書型配列
# [全文]
# [[文章1][文章2]]
# [[[形態素1][形態素2]][[形態素3][形態素4]]]
# 上記のように返ってくる

import requests
import json



appid = "2209ee67bfcb549e49c8f8c08da3f5a837a4085782abe759bafa5de02d7a4dc0"
request_url = "https://labs.goo.ne.jp/api/morph"

def keitaiso(honbun):
    req_json = {
        'app_id' : appid,
        'sentence' : honbun,
        'info_filter' : "form|pos"
    }

    res = requests.post(request_url,json=req_json)
    res_json = res.json()
    d = res_json['word_list']

    return d



