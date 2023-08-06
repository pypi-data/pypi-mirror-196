import datetime
import pandas as pd
from sqlalchemy.engine import create_engine
import matplotlib.pyplot as plt
import traceback
import requests
from lxml import etree
import json
from environs import Env
from random import random,randint


# env = Env()
# env.read_env()


# today = str(datetime.date.today())
# lastmonth=str(datetime.date.today()-datetime.timedelta(days=30))
# connect_info = env.str("CONNECT_INFO")
# engine = create_engine(connect_info)#,max_overflow=50



#获取单个A股某级别的指定类型的1000条K线数据
def dk_soure_subscr(code,ktype,select='tencent'):#为其他网站接入留扩展口yahoo,baidu,tencent
    '''获取基础价格数据，ktype取值范围[1,5,30,240]，对应1m线，5m线，30m线，日线，code格式SH.600***,SZ.002***'''
    select = randint(0,1)
    s_list = ['sina','tencent']
    select = s_list[select]
    try:
        if select == 'sina':
            scale = ktype
            dk = sina_api(code,scale)
        elif select == 'tencent':
            scale = ktype
            dk = tencent_api(code,scale,start='',end='',numb=640)
        return dk
    except:
        traceback.print_exc()
        print('****************订阅出现错误*********************')


def sina_api(code,scale):
    code_ = code[:2].lower() + code[3:]
    params={
        'headers':{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'},
        # 'stream':True,#下载大文件时配合以下方式使用for chunk in r.iter_content(chunk_size=512):f.write(chunk)
        }
    # https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000300&scale=240&ma=no&datalen=1025
    url = f'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={code_}&scale={scale}&ma=no&datalen=1025'
    r = requests.get(url,params=params)
    r.encoding = 'gbk'
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print(type(r.text))
    # r = etree.HTML(r.text)
    r = pd.DataFrame(json.loads(r.text))
    r['time_key'] = r['day']
    r['open'] = r['open'].astype(float)
    r['close'] = r['close'].astype(float)
    r['high'] = r['high'].astype(float)
    r['low'] = r['low'].astype(float)
    r['volume'] = r['volume'].astype(float)
    # code_n = code[:2].upper() + '.' + code[2:]
    r['code'] = [code] * len(r)
    r = r[['code','time_key','open','close','high','low','volume']]
    # print(r)re
    return r


#从腾讯获取历史k线数据
def tencent_api(code,scale,start='',end='',numb=500):
    code_ = code[:2].lower() + code[3:]
    params={
        'headers':{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'},
        # 'stream':True,#下载大文件时配合以下方式使用for chunk in r.iter_content(chunk_size=512):f.write(chunk)
        }
    rad =  random()   
    # print(rad)
    if scale == '240':
        #日线图
        url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?' \
                    f'param={code_},day,{start},{end},{numb},qfq&r={rad}'
        r = requests.get(url,params=params)
        r.encoding = 'gbk'
        r = json.loads(r.text)
        try:
            r = r['data'][code_]['qfqday']
        except:
            r = r['data'][code_]['day']
        r = pd.DataFrame(r)#1,2,3,4开盘，收盘，最高，最低
        r[0] = pd.to_datetime(r[0])
        # print(r)
    else:
        #1分钟图
        url = 'https://ifzq.gtimg.cn/appstock/app/kline/mkline?param=' \
                f'{code_},m{scale},{end},{numb}&_var=m{scale}_today&r={rad}'
        r = requests.get(url,params=params)
        r.encoding = 'gbk'
        # print(r)
        # print(r.status_code)
        # print(r.text)
        # print(type(r.text))
        index = r.text.find('=') + 1
        r = r.text[index:]
        # print(r)#去点前面的'fdays_data_sh600000='
        r = json.loads(r)
        r = r['data'][code_][f'm{scale}']
        r = pd.DataFrame(r)#1,2,3,4开盘，收盘，最高，最低
        r[0] = pd.to_datetime(r[0])
        # print(r)
    r['time_key'] = r[0].astype(str)
    r['open'] = r[1].astype(float)
    r['close'] = r[2].astype(float)
    r['high'] = r[3].astype(float)
    r['low'] = r[4].astype(float)
    r['volume'] = r[5].astype(float)*100
    r['code'] = [code] * len(r)
    r = r[['code','time_key','open','close','high','low','volume']]
    # print(r)
    if scale == '1':
        r = merge_930(r)
    # print(r)
    return r


#把取到的1m数据的9：30合并入9：31中，ft数据源特有
def merge_930(dk):
    drop_list = []
    for i in dk.index[:-1]:
        if dk.loc[i,'time_key'][-8:]=='09:30:00' and dk.loc[i+1,'time_key'][-8:]=='09:31:00':
            dk.loc[i+1,'volume'] = dk.loc[i+1,'volume'] + dk.loc[i,'volume']
            dk.loc[i+1,'open'] = dk.loc[i,'open']
            drop_list.append(i)
    dk.drop(drop_list,inplace=True)
    dk = dk.reset_index(drop=True)#不重新定义index会使得calculate_macd索引出错
    return dk
