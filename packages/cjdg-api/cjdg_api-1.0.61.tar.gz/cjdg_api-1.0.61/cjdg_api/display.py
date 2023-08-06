# 新陈列2.0-指导任务

import requests
from .base import base


class display(base):
    def __init__(self, token):
        super().__init__(token)

    
    # 指导任务默认列表
    def list(self):
        api_name = 'display/display/task/list'
        return self.request(api_name)

# def logon():
#     api_name = 'http://it.xxynet.com/shopguide/api/auth/logon'
#         # heads = {'qqq':'wq'}
#     data = {'loginName':"",
#         "password":'',
#         'version':1}
#     res = requests.post(api_name,data=data)
#     print(res.text)

# logon()

