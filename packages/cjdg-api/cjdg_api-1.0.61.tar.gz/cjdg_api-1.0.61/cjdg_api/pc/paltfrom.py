'''
@Author  :   顾一龙 
@Time    :   2023/03/10 17:11:16
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......


from cjdg_api.base import baseApixxYent


class paltFrom(baseApixxYent):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)


# 周榜,月榜（0 or 1的区别）
    def getCycleList(self,data):
        api_name = "enter/superguide/platformRanking/userLearningLength/getCycleList"
        return self.request(api_name=api_name,data=data)
    

    def findRanking(self,data):
        api_name = "enter/superguide/platformRanking/userLearningLength/findRanking"
        return self.request(api_name=api_name,data=data)
    



def main():
    a= paltFrom(token="4720a82584e516f2237149864aeefa31_goso_web")
    aaa = {"data":{"cycleTypes":1,"num":7}}
    rows = a.getCycleList(data=aaa)
    print(rows)


if __name__ == '__main__':
    main()