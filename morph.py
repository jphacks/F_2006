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


#リストを分解し、単語ごとにリスト型にして出力する
#今現在は名詞区切り


di = [[['おはようございます', '独立詞'], [' ', '空白'], ['今日', '名詞'], ['は', '連用助詞'], ['10月', '名詞'], ['31日', '名詞'], ['です', '判定詞']]] 

def tangoseisei(d):
    tango_ls = []
    s = ''
    for first in d:
        for second in first:
            if(second[1] != '名詞'):
                s = s+second[0]
            else:
                if(s != ''):
                    tango_ls.append(s)
                s = second[0]
    tango_ls.append(s)
    return tango_ls


def morph(string):
    return tangoseisei(keitaiso(string))




