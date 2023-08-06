import requests
import re
import pandas as pd
import json
import numpy as np
from mtmtool.io import read_yaml


class TianTianFund:
    def __init__(self, headers_file:str) -> None:
        self.headers_file = headers_file
        self.headers = read_yaml(headers_file)
        pass
    
    def get_fund_daily_worth(self, fund_code, start_date, end_date, page_size=20):
        # 获取基金每日净值
        url = f"http://api.fund.eastmoney.com/f10/lsjz?fundCode={fund_code}&pageIndex=1&pageSize={page_size}&startDate={start_date}&endDate={end_date}"
        resp = requests.get(url, headers=self.headers)
        res = json.loads(resp.text)
        df = pd.DataFrame(res["Data"]["LSJZList"])
        df = df.replace("", np.nan, inplace=False).replace("---", np.nan, inplace=False)
        df.set_index('FSRQ', inplace=True)
        return df

    def get_fund_holder_structure(self, fund_code):
        # 获取基金持仓结构
        url = f'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=cyrjg&code={fund_code}'
        resp = requests.get(url)
        pattern = r"<tr><td>(.*?)</td><td class='tor'>(.*?)</td><td class='tor'>(.*?)</td><td class='tor'>(.*?)</td><td class='tor'>(.*?)</td></tr>"
        res = re.findall(pattern, resp.text.replace("%", ""))
        df = pd.DataFrame(res, columns=['公告日期', '机构持有比例(%)', '个人持有比例(%)', '内部持有比例(%)', '总份额（亿份）'])
        df.set_index('公告日期', inplace=True)
        df = df.replace("", np.nan, inplace=False).replace("---", np.nan, inplace=False)
        df = df.astype(float, copy=False)
        return df

    def get_fund_rank(self, start_date:str, end_date:str, page_size = 1000):
        # 获取基金排行
        url = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=1nzf&st=desc&sd={start_date}&ed={end_date}&qdii=&tabSubtype=,,,,,&pi=1&pn={page_size}&dx=1&v=0.037434531760037526'
        resp = requests.get(url, headers=self.headers)
        pattern = r"var rankData =.*datas:(.*?),allRecords.*;"
        res = re.findall(pattern, resp.text)
        res = json.loads(res[0])
        res = [i.split(",") for i in res]
        df = pd.DataFrame(res)
        df = df.iloc[:, :17]
        df = df.replace("", np.nan, inplace=False)
        df.columns = ['基金代码', '基金简称', "首拼",'日期', '单位净值', '累计净值', '日增长率', '近1周', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '今年来', '成立来', '发行日']
        return df
        