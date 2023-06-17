#=================BiliBili日出东水===================
#               o365日历获取测试Demo
#----------------------------------------------------

from O365 import Account
import datetime
import time
import os
from collections import OrderedDict
from datetime import timezone
from configparser import ConfigParser

rootPath = os.path.abspath(os.path.dirname(__file__))
cfg = ConfigParser()
cfg.read(rootPath + "/config.ini",encoding="utf-8")
config = cfg.items("OutlookWeatherCalendar")
credentials = (config[0][1], config[1][1])

#这里填写客户端ID   #API权限中的值(第一次生成时才能看到)

print("")
print("=================Outlook令牌生成工具===================")
print("")
print("请提前在config.ini文件填写客户端ID,和密码的值")
print("")
print("复制下面的连接到浏览器,并登录邮箱授权,然后将浏览器链接粘贴回来,并回车")
print("")
print("-注意不要有任何多余空格和符号!")
print("")
print("------------------BiliBili日出东水---------------------")
print("")

if(os.path.exists(rootPath + "/o365_token.txt")==False):
    account = Account(credentials)
    if account.authenticate(scopes=['basic', 'calendar_all']):
        print('Authenticated! 令牌生成成功!')
else:
    print("info: 检测到o365_token.txt令牌文件,使用该令牌获取日程,如有错误请删除重新生成")
    print("")


#如想查看所有event属性,可以查看源代码,在976行开始,搜索所有的 @property
#https://github.com/O365/python-o365/blob/412d5b7dc521328ceb84a0086f1d89036bc09bd8/O365/calendar.py

def GetO365(maxCount):
    try:
        account = Account(credentials)
        schedule = account.schedule()
    except :
        print("配置错误,请检查")
        return
    
    #查询从今天开始一个月内的日历
    #也可以指定 datetime(2022, 5, 30)
    now_time = datetime.datetime.now()
    end_time = datetime.timedelta(days =30)
    range_time = (now_time + end_time).strftime('%Y-%m-%d')

    q = schedule.new_query('start').greater_equal(now_time)
    q.chain('and').on_attribute('end').less_equal(range_time)

    getSchedule = schedule.get_events(query=q, include_recurring=True) 
    
    scheduleDic = OrderedDict()
    scheduleCount = 0
    for event in getSchedule:
        #获取位置
        locationStr = str(event.location).split(",")[0].split(":")[1].replace("'","").replace(" ","")
        #获取时间
        dateTime = event.start
        #获取标题
        subjectStr = event.subject
        #获取正文
        bodyStr = str(event.body)
        startIndex = bodyStr.find("body")
        endIndex = bodyStr.find("/body")
        bodyProcessStr = bodyStr[startIndex+6:endIndex-1].replace("\n","")

        elemDic = OrderedDict()
        elemDic["location"] = locationStr
        elemDic["dateTime"] = dateTime
        elemDic["subjectStr"] = subjectStr
        elemDic["bodyStr"] = bodyProcessStr
        scheduleDic[scheduleCount] = elemDic
        scheduleCount+=1
        if scheduleCount >=maxCount:
            break
    return scheduleDic


scheduleDic = GetO365(5)
print("\n查询近一个月日程: "+str(len(scheduleDic))+"\n")

for x in scheduleDic:
    print("位置: "+ scheduleDic[x]["location"])
    t = scheduleDic[x]["dateTime"]
    print("时间: "+ str(t.month) +"月"+ str(t.day)+"日" + str(t.strftime('%H:%M')))
    print("标题: "+ scheduleDic[x]["subjectStr"])
    print("正文: "+ scheduleDic[x]["bodyStr"])
    print("\n---------------------\n")



print("按任意键退出......")
input()



#新建日历事件
#创建一个新事件
#new_event = schedule.new_event()  
#new_event.subject = '这里写标题'
#new_event.location = '位置'
#时间
#new_event.start = dt.datetime(2022, 4, 18, 19, 45)
#设置重复
#new_event.recurrence.set_daily(1, end=dt.datetime(2022, 4, 19))
#提前提醒时间
#new_event.remind_before_minutes = 45 
#更新保存
#new_event.save() 

#发送邮件
#m = account.new_message()
#m.to.add('XXXXXXX@qq.com')
#m.subject = 'Testing!'
#m.body = "这里写正文"
#m.send()


