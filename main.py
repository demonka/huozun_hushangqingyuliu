#!/usr/bin/env python3
#coding=utf8

import json
import os,sys
import requests
import random
from collections import Counter


huozun_id="2003884457"       #霍尊
pingan_id="1237530023"       #平安
timo_id="1726379140"         #田汨
songsiheng_id="1389135857"   #宋思衡
zhengwei_id="1412398173"     #郑伟
andong_id= "1717783440"      #安栋
tianchenming_id="1607192000" #田辰明
ganshijia_id="1404064013"    #甘世佳
tuhuabing_id="2622511651"    #屠化冰
yanjun_id="1725681421"       #严俊
huyang_id="1749261823"       #胡洋
                             #薛钦之 weibo连夜注销
                             #李培境  未找到weibo账号，但估计没跑了





class HuoZun(object):
    def __init__(self):
        self.out_path=os.path.join(os.path.abspath("."),"data")
        self.all_focus_list=f"{self.out_path}/all_focus_list.json"
        self.close_relation=f"{self.out_path}/close_relation.json"
        self.user_list=[
            huozun_id,pingan_id,timo_id,songsiheng_id,zhengwei_id,andong_id,tianchenming_id,ganshijia_id,tuhuabing_id,yanjun_id,huyang_id
        ]

    def GenHeader(self):
        user_agents=[
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edg/92.0.902.67",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "UCWEB7.0.2.37/28/999",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        ]
        headers = {
            'Cookie': 'ALF=1584682452; SCF=Ao1AQDSyNMyR23TDx5xG_IJe2v4XqtrohlDD67o143N_ilDj19QP-Ffy2qe6e9RCYw2cmt-buWEsw2I7h1PUgm8.; SUB=_2A25zSLo0DeRhGeFM4lUZ9yrJwj6IHXVQssZ8rDV6PUJbktANLXfDkW1NQIfd1Q7IIALrtuY8yxDNe-TWrxqGr9QJ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-dpVkFAo9J5yWOxXdB82b5JpX5K-hUgL.FoME1KMRS0Bf1Kz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeo.N1hMXSK.E; SUHB=0rr7f9X9Ndnx8q; _T_WM=52236839197; XSRF-TOKEN=9d35ef; WEIBOCN_FROM=1110006030; MLOGIN=1',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': random.choice(user_agents)
        }
        return headers

    def GetFocusList(self,uid):
        focus_list=[]
        url=f"https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FOLLOWERS&page="  
        index=0
        while True:
            result=requests.get(url+str(index),headers=self.GenHeader())
            if result.status_code!=200:
                print("返回码不是200，退出")
                sys.exit(1)
            resp_data=result.json()['data'] 
            if "cards" not in  resp_data:
                break
            focus_list+=resp_data['cards']
            index+=1
        return focus_list

    def GetALLFocusList(self):
        all_focus_list=[]
        for user_id in self.user_list:
            all_focus_list.append({"id":user_id,"focusList":self.GetFocusList(user_id)})
        if not os.path.exists(self.all_focus_list):
            with open(self.all_focus_list,"w+") as f:
                json.dump(all_focus_list,f,ensure_ascii=False)

    def ParseData(self):
        all_focus_list=[]
        with open(self.all_focus_list,'r+') as f:
            data=json.load(f)
        for user_data in data:
            for user_focus in user_data['focusList']:
                all_focus_list.append(user_focus['user']['screen_name'])
        focus_frequency=sorted(list(dict(Counter(all_focus_list)).items()),key=lambda x:-x[1])
        with open(self.close_relation,'w+') as f:
            json.dump(focus_frequency,f,ensure_ascii=False)

    def Main(self):
        if not os.path.exists(self.all_focus_list):
            self.GetALLFocusList()
        self.ParseData()

if __name__=="__main__":

    h=HuoZun()
    h.Main()