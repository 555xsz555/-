from DrissionPage import WebPage
import time
from pprint import pprint
import numpy as np
import pandas as pd
db = WebPage()

shuju='https://re.m.jd.com/page/homelike/rec?'
db.listen.start(shuju)
time.sleep(2)

url = 'https://re.m.jd.com/page/homelike?ad_od=3&re_dcp=21Sm2D2ZOw&traffic_source=1004&bd_vid=c07a785bd447e8ea&cu=true&utm_source=haosou-search&utm_medium=cpc&utm_campaign=t_262767352_haosousearch&utm_term=61861202133_0_5185d780e3c64d119d28171bbe616c5a'
db.get(url)
time.sleep(2)
lst = []
for i in range(2):

    db.scroll.to_bottom()

    resp = db.listen.wait()

    json_data = resp.response.body

    pprint(json_data)
    # for i in json_data['data']:
    #     a=i['title']
    #     print('>>>',i['title'])
    #     lst.append(a)

    for i in json_data['data']:
        a1 = i['title']
        print('标题', i['title'])
        a2 = i['cc']
        print('评论数', i['cc'])
        a3 = i['fp']
        print('商品价格', i['fp'])
        a4 = i['price']
        print('商品原价格', i['price'])
        try:
            a5 = i['gcp']
            print('商品好评率', i['gcp'])
        except:
            a5 = None
        lst.append(
            {
                '标题': a1,
                '评论数': a2,
                '商品价格': a3,
                '商品原价格': a4,
                '商品好评率': a5
            }
        )
    print('-----------------------------')
    print(lst)
    df = pd.DataFrame(lst)
    print(df)
    print(df.isna().sum())
    df = df.fillna(df[['商品好评率']].mean())
    print(df[['商品好评率']])
    print('进行空字符串的转化')
    df['商品价格'] = df['商品价格'].replace('', np.nan)
    df['评论数'] = df['评论数'].replace('', '0')
    print('==========================')
    print(df.isnull().sum())
    df = df.fillna({'商品价格': 0})
    print(df.isnull().sum())
    print(df.duplicated())
    print(df.dtypes)

    print('----------------------------')
    print('进行数据类型的转换')
    df['商品价格'] = df['商品价格'].astype('float64')
    df['商品原价格'] = df['商品原价格'].astype('float64')
    print(df.dtypes)
    print(df.info())
    print('==================================')
    print(df.describe())
    pprint(df.value_counts())
    print('进行数值型统计描述')
    num_cols = ['评论数', '商品价格', '商品原价格', '商品好评率']
    print(df[num_cols].describe())
    print('over')
print(lst)
print(len(lst))