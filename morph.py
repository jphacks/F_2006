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
    bunsho = honbun.split('\n')
    load_buf = ''
    tango_ls = []

    for danraku in bunsho:
        if (len(load_buf) + len(danraku) < 10000):
            load_buf = load_buf + danraku
        else:
            last_req_json = {
                'app_id' : appid,
                'sentence' : load_buf,
                'info_filter' : "form|pos"
            }

            last_res = requests.post(request_url,json=last_req_json)
            last_res_json = last_res.json()
            tango_ls = tango_ls + tangoseisei(last_res_json['word_list'])
            load_buf = danraku

    last_req_json = {
        'app_id' : appid,
        'sentence' : load_buf,
        'info_filter' : "form|pos"
    }

    last_res = requests.post(request_url, json=last_req_json)
    last_res_json = last_res.json()
    tango_ls = tango_ls + tangoseisei(last_res_json['word_list'])

    return tango_ls


#リストを分解し、単語ごとにリスト型にして出力する
#今現在は名詞区切り

limitter = 7   # 字数制限

def tangoseisei(d):
    tango_ls = []
    buf_str = ''
    skip = False
    for first in d:                 # 各文情報を取得
        for tango_info in first:    # 各単語情報を取得
            if(tango_info[1] == '空白'):    # 空白の場合
                if (buf_str != ''):
                    tango_ls.append(buf_str)
                    buf_str = ''

            elif(tango_info[1] == '句点'):  # 句点の場合、含めたものを分割したうえで一度空白を挟む
                buf_str = buf_str + tango_info[0]
                tango_ls.append(buf_str)
                for i in range(2):
                    tango_ls.append('')
                buf_str = ''
            
            elif(tango_info[1] == '読点'):  # 読点の場合、含めたものを分割する
                buf_str = buf_str + tango_info[0]
                tango_ls.append(buf_str)
                buf_str = ''

            elif(skip):                     # 前の単語が冠動詞などで有無を言わさず接続する場合
                added_l = len(buf_str + tango_info[0])
                if (added_l > limitter):
                    tango_ls.append(buf_str)
                    buf_str = tango_info[0]
                else:
                    buf_str = buf_str + tango_info[0]
                skip = False

            elif(
                tango_info[1] == '名詞' or
                tango_info[1] == '動詞語幹' or
                tango_info[1] == '補助名詞' or
                tango_info[1] == '形容詞語幹' or
                tango_info[1] == '連体詞' or
                tango_info[1] == '連用詞' or
                tango_info[1] == '接続詞' or
                tango_info[1] == '独立詞'
                ):
                if(buf_str != ''):
                    tango_ls.append(buf_str)
                buf_str = tango_info[0]

            elif(                           # 次の単語を必ず一文節としてこの後に続ける場合
                tango_info[1] == '冠名詞' or
                tango_info[1] == '冠動詞' or
                tango_info[1] == '冠形容詞' or
                tango_info[1] == '冠数詞'):
                if (buf_str != ''):
                    tango_ls.append(buf_str)
                buf_str = tango_info[0]
                skip = True

            else:                           # その他
                added_l = len(buf_str + tango_info[0])
                if (added_l > limitter):
                    tango_ls.append(buf_str)
                    buf_str = tango_info[0]
                else:
                    buf_str = buf_str + tango_info[0]
                
    tango_ls.append(buf_str)
    return tango_ls


def morph(string):
    return keitaiso(string)
