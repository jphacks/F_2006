# 受け取った文章を形態素解析して返す
# 型は辞書型配列
# [全文]
# [[文章1][文章2]]
# [[[形態素1][形態素2]][[形態素3][形態素4]]]
# 上記のように返ってくる

<<<<<<< HEAD
class tango_data:
    def __init__(self):
        self.str = ''
        self.kanmuri = False
        self.buntou = False


kanmuri_list = ['冠名詞','冠動詞','冠形容詞','冠数詞','連体詞'] #冠系統のもの、これらがきたら次の文頭を虫する
head_list = ['名詞','動詞語幹','形容詞語幹'] #文頭にこれらのものがきたら、一つ前までを表示させるようにする
bunmatu_list = [] #文末にこれらのものがきたら、そこまでで出力(文頭あればいらないかも)

import requests
import json


=======
import requests
import json

>>>>>>> 8bc043907405d9b36ef39f3c2f0c03257481244b
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

<<<<<<< HEAD
def tangoseisei(d):
    tango_ls = []
    s = tango_data()
    for first in d:
        for second in first:
            if(second[1] in kanmuri_list):#冠だったとき
                if(s.str == ''):
                    s.str = second[0]
                    s.kanmuri = True
                else:
                    tango_ls.append(s.str)
                    s.str = second[0]
                    s.kanmuri = True

            elif(second[1] in head_list):#文頭だったとき
                if(s.str == ''):
                    s.str = second[0]
                elif(s.kanmuri):
                    s.str = s.str+second[0]
                    s.kanmuri = False
                else:
                    tango_ls.append(s.str)
                    s.str = second[0]

            else:#どれでもないとき
                if(s == ''):
                    s.str = second[0]
                else:
                    s.str = s.str+second[0]
    if(s.str != ''):#最後に残っているものを追加            
        tango_ls.append(s.str)
=======

di = [[['おはようございます', '独立詞'], [' ', '空白'], ['今日', '名詞'], ['は', '連用助詞'], ['10月', '名詞'], ['31日', '名詞'], ['です', '判定詞']]] 

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

            elif(skip):                     # 前の単語が冠動詞などで有無を言わさず接続する場合
                skip = False
                buf_str = buf_str+tango_info[0]     

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
                buf_str = buf_str + tango_info[0]
                
    tango_ls.append(buf_str)
>>>>>>> 8bc043907405d9b36ef39f3c2f0c03257481244b
    return tango_ls


def morph(string):
    return tangoseisei(keitaiso(string))
<<<<<<< HEAD

n = 'このりんごは赤いです。このバナナは黄色いです。'

print(morph(n))




=======
>>>>>>> 8bc043907405d9b36ef39f3c2f0c03257481244b
