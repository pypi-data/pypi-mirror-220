import requests
from requests.cookies import RequestsCookieJar
from mtmtool.io import read_yaml
import pandas as pd

class JointQuant:
    def __init__(self, headers_file:str) -> None:
        self.headers_file = headers_file
        self.headers_raw = read_yaml(headers_file)
        self.headers = self.headers_raw.copy()
        del self.headers["Cookie"]
        self.cookie_raw = self.headers_raw["Cookie"]
        pass

    def get_cookie_jar(self):
        cookies = {i.split("=")[0]: i.split("=")[1] for i in self.cookie_raw.split("; ")}
        cookieJar = RequestsCookieJar()
        for i in cookies:
            cookieJar.set(i, cookies[i], domain=self.headers_raw["Host"])
        return cookieJar
    
    def login_web(self, username, password):
        self.session = requests.Session()
        data = {
            "CyLoginForm[username]": username,
            "CyLoginForm[pwd]": password
        }
        self.session.cookies = self.get_cookie_jar()
        resp = self.session.post("https://www.joinquant.com/user/login/doLogin", data=data, headers=self.headers)
        resp = self.session.get("https://www.joinquant.com/user/index/isLogin", headers=self.headers)
        isLogin = resp.json()["data"]["isLogin"]
        return isLogin==1

    def run_strategy(self, file, start_date, end_date):
        data = read_yaml(file)
        data["backtest[startTime]"] = start_date
        data["backtest[endTime]"] = end_date
        url = "https://www.joinquant.com/algorithm/index/build?ajax=1"
        resp = self.session.post(url, data=data, headers=self.headers)
        print(resp.text)
        resp_json = resp.json()["data"]
        algorithmId = resp_json["algorithmId"]
        backtestId = resp_json["backtestId"]
        backtestId_ = resp_json["backtestId_"]
        tradeDays = resp_json["tradeDays"]
        return algorithmId, backtestId, backtestId_, tradeDays
    
    def until_strategy_finish(self, file, backtestId, sleep_seconds=1):
        import time
        needSecondsLast = 0
        while True:
            needSeconds = self.track_strategy_runtime(file, backtestId)
            if needSeconds == needSecondsLast and needSeconds != 0:
                break
            else:
                needSecondsLast = needSeconds
                time.sleep(sleep_seconds)
        return needSeconds

    def track_strategy_runtime(self, file, backtestId):
        strategy_data = read_yaml(file)
        token = strategy_data["token"]
        url = f"https://www.joinquant.com/algorithm/backtest/runTimeInfo?token={token}&backtestId={backtestId}"
        resp = self.session.get(url, headers=self.headers)
        resp_data = resp.json()["data"]
        needSeconds = resp_data["needSeconds"]
        return needSeconds
    
    def track_strategy_log(self, file, backtestId):
        strategy_data = read_yaml(file)
        url = f"https://www.joinquant.com/algorithm/backtest/log?backtestId={backtestId}&offset=0&ajax=1"
        data = {
            "undefined": "", 
            "ajax": 1,
            "token": strategy_data["token"],
        }
        resp = self.session.post(url, data=data, headers=self.headers)
        print(resp.text)
        resp_data = resp.json()["data"]
        logArr = resp_data["logArr"]
        return logArr