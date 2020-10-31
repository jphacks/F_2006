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
                tango_ls.append(s)
                s = second[0]
    tango_ls.append(s)
    return tango_ls



