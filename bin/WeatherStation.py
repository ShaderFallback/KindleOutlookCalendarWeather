#=================BiliBili日出东水===================
#                   墨水屏天气台历
#----------------------------------------------------
import sys
import os
import http.server
import socketserver
import socket
rootPath = os.path.abspath(os.path.dirname(__file__))
#rootPath = os.path.split(curPath)
#sys.path.append(curPath + "/lib")
fontPath = rootPath + "/lib/font.ttf"
import time
from PIL import Image,ImageDraw,ImageFont,ImageChops
import traceback
import datetime
import requests
import logging
from O365 import Account
from collections import OrderedDict
import re
import threading
from configparser import ConfigParser
import feedparser
import math
fontSize16 = ImageFont.truetype(fontPath, 16)
fontSize20 = ImageFont.truetype(fontPath, 20)
fontSize25 = ImageFont.truetype(fontPath, 25)
fontSize30 = ImageFont.truetype(fontPath, 30)
fontSize60 = ImageFont.truetype(fontPath, 60)
fontSize70 = ImageFont.truetype(fontPath, 70)

oilStrTime = ""
weekStr = ""
oilStrWeek = ""
countUpdate_1 = False
countUpdate_2 = False
countUpdate_3 = False
countUpdate_4 = False
SwitchDay = True
tempArray = ["---"]*23
scheduleDic = OrderedDict()
scheduleDic2 = OrderedDict()
pathStrList = [""]*2
clearCount = 0
cfg = ConfigParser()
cfg.read(rootPath + "/config.ini",encoding="utf-8")
config = cfg.items("OutlookWeatherCalendar")
switchRss = True
nowPage = 0
minDicCount = 0
unitCount = int(10) #每页显示新闻数量
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0"
}

def GetTime():
    return(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"   ")

rootPath = os.path.abspath(os.path.dirname(__file__))
print(GetTime() + "RootPath: "+ rootPath)

def DatetimeNow():
    #如果启用网页服务器的话,前一分钟生成好图片
    if int(config[4][1]) == 1:
        return datetime.datetime.now() + datetime.timedelta(minutes = 1)
    else:
        return datetime.datetime.now() #+ datetime.timedelta(hours = 8)

def GetO365(maxCount):
    global scheduleDic
    global config
                    #这里填写客户端ID                       #API权限中的值(第一次生成时才能看到)
    credentials = (config[0][1], config[1][1])
    account = Account(credentials)
    schedule = account.schedule()
    #查询从今天开始一个月内的日历
    #也可以指定 datetime(2022, 5, 30)
    now_time = DatetimeNow()
    end_time = datetime.timedelta(days =30)
    range_time = (now_time + end_time).strftime('%Y-%m-%d')

    q = schedule.new_query('start').greater_equal(now_time)
    q.chain('and').on_attribute('end').less_equal(range_time)

    getSchedule = schedule.get_events(query=q, include_recurring=True)     
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

#获取天气
def GetTemp():
    global config
    try:                                                                     # 连接超时,6秒，下载文件超时,7秒
        r = requests.get('http://t.weather.itboy.net/api/weather/city/'+config[2][1],timeout=(6,7)) 
        r.encoding = 'utf-8'
        tempList = [
        (r.json()['cityInfo']['city']),             #城市0
        (r.json()['data']['shidu']),                #湿度1
        (r.json()['data']['forecast'][0]['low']),   #今日低温2
        (r.json()['data']['forecast'][0]['high']),  #今日高温3
        (r.json()['data']['forecast'][0]['type']),  #今日天气4
        (r.json()['data']['forecast'][0]['fx']),    #今日风向5
        (r.json()['data']['forecast'][0]['fl']),    #今日风级6

        (r.json()['data']['forecast'][1]['low']),   #明日低温7
        (r.json()['data']['forecast'][1]['high']),  #明日高温8
        (r.json()['data']['forecast'][1]['type']),  #明日天气9
        (r.json()['data']['forecast'][1]['fx']),    #明日风向10
        (r.json()['data']['forecast'][1]['fl']),    #明日风级11

        (r.json()['data']['forecast'][2]['low']),   #后日低温12
        (r.json()['data']['forecast'][2]['high']),  #后日高温13
        (r.json()['data']['forecast'][2]['type']),  #后日天气14
        (r.json()['data']['forecast'][2]['fx']),    #后日风向15
        (r.json()['data']['forecast'][2]['fl']),    #后日风级16

        (r.json()['data']['forecast'][3]['low']),   #大后日低温17
        (r.json()['data']['forecast'][3]['high']),  #大后日高温18
        (r.json()['data']['forecast'][3]['type']),  #大后日天气19
        (r.json()['data']['forecast'][3]['fx']),    #大后日风向20
        (r.json()['data']['forecast'][3]['fl']),    #大后日风级21

        (r.json()['cityInfo']['updateTime'])        #更新时间22
        ]
    except Exception as e:
        tempList = ["---"]*23
        print(GetTime() + 'Update Weather...Fail'+str(e), flush=True)
        return tempList
    else:
        return tempList

def UpdateWeatherIcon(tempType):  #匹配天气类型图标
    if(tempType == "大雨"  or tempType == "中到大雨"):
        return "heavyRain.bmp"
    elif(tempType == "暴雨"  or tempType == "大暴雨" or 
        tempType == "特大暴雨" or tempType == "大到暴雨" or
        tempType == "暴雨到大暴雨" or tempType == "大暴雨到特大暴雨"):
        return "rainstorm.bmp"
    elif(tempType == "沙尘暴" or tempType == "浮尘" or
        tempType == "扬沙" or tempType == "强沙尘暴" or
        tempType == "雾霾"):
        return "sandstorm.bmp"
    elif(tempType == "晴"):
        return "sunny.bmp"
    elif(tempType == "阴"):
        return "cloudy.bmp"
    elif(tempType == "多云"):
        return "partlyCloudy.bmp"
    elif(tempType == "小雨"):
        return "lightRain.bmp"
    elif(tempType == "中雨"):
        return "moderateRain.bmp"
    elif(tempType == "阵雨"):
        return "shower.bmp"
    elif(tempType == "雷阵雨"):
        return "thunderShower.bmp"
    elif(tempType == "小到中雨"):
        return "lightModerateRain.bmp"
    elif(tempType == "雷阵雨伴有冰雹"):
        return "thunderShowerHail.bmp"
    elif(tempType == "雾"):
        return "fog.bmp"
    elif(tempType == "冻雨"):
        return "sleet.bmp"
    elif(tempType == "雨夹雪"):
        return "rainSnow.bmp"
    elif(tempType == "阵雪"):
        return "snowShower.bmp"
    return "noWeatherType.bmp"

def TodayWeek(nowWeek):
    if nowWeek == "0":
        return"星期天"
    elif nowWeek =="1":
        return"星期一"
    elif nowWeek =="2":
        return"星期二"
    elif nowWeek =="3":
        return"星期三"
    elif nowWeek =="4":
        return"星期四"
    elif nowWeek =="5":
        return"星期五"
    elif nowWeek =="6":
        return"星期六"

def UpdateData():
    global tempArray
    tempArray = GetTemp()
    return tempArray

def UpdateTemp(timeUpdate):
    global oilStrWeek
    global tempArray
    global countUpdate_1
    global countUpdate_2
    global countUpdate_3
    global countUpdate_4
    strtime2 = timeUpdate.strftime('%H:%M')   #时间
    strtime4 = timeUpdate.strftime('%w')      #星期
    strtime5 = timeUpdate.strftime('%H')      #小时
    
    if(strtime4 != oilStrWeek):  #每天重置更新天气
        oilStrWeek = strtime4
        countUpdate_1 = True
        countUpdate_2 = True
        countUpdate_3 = True
        countUpdate_4 = True
        tempArray = UpdateData()
        #epd.Clear()
        print(GetTime()+'Reset Update...ok', flush=True)

    # 天气API 只有这几个点会更新,减少无用请求
    intTime = int(strtime5)

    if(countUpdate_1 and  intTime == 7):
        tempArray = UpdateData()
        countUpdate_1 = False
        print(GetTime() + 'Update Weather...ok', flush=True)
    elif(countUpdate_2 and intTime == 11):
        tempArray = UpdateData()
        countUpdate_2 = False
        print(GetTime() + 'Update Weather...ok', flush=True)
    elif(countUpdate_3 and intTime == 16):
        tempArray = UpdateData()
        countUpdate_3 = False
        print(GetTime() + 'Update Weather...ok', flush=True)
    elif(countUpdate_4 and intTime == 21 ):
        tempArray = UpdateData()
        countUpdate_4 = False
        print(GetTime() + 'Update Weather...ok', flush=True)

def ReplaceLowTemp(lowTemp):
    temp_L = lowTemp.replace("低温","")
    temp_L = temp_L.replace("℃","")
    temp_L = temp_L.replace(" ","")
    return temp_L

def ReplaceHeightTemp(heighTemp):
    temp_H = heighTemp.replace("高温","")
    temp_H = temp_H.replace("℃","")
    temp_H = temp_H.replace(" ","")
    return temp_H

#348 - 640 像素 居中显示
#居中显示的方法 一个字宽度30像素 例如从479像素开始 多加一个字 少空 15 个像素
def AlignCenter(string,scale,startPixel):
    charsCount = 0
    for s in string:
        charsCount += 1
    charsCount *= scale/2
    charsCount = startPixel - charsCount
    return charsCount

def StrLenCur(text):
    #字母和数字占位与汉字间距不同 
    #2个约等于一个汉字,当包含数字或字母时放宽显示数量
    allStrLen = len(text)
    numberLen = len("".join([x for x in text if x.isdigit()]))
    letterLen = len("".join(re.findall(r'[A-Za-z]',text)))
    sumLen = (numberLen + letterLen)
    characterLen =  allStrLen - sumLen
    calculateLen = characterLen + int(sumLen/3)
    tempLen = (int)(sumLen/3) + 17
    if(calculateLen >= 17):
        return text[0:tempLen]+"..."
    else:
        return text

def DrawHorizontalDar(draw,Himage,timeUpdate):
    strtime = timeUpdate.strftime('%Y-%m-%d') #年月日
    strtime2 = timeUpdate.strftime('%H:%M')   #时间
    strtimeW = timeUpdate.strftime('%w') #星期

    #显示星期
    draw.text((34, 30), TodayWeek(strtimeW), font = fontSize30, fill = 0)
    #显示时间   
    draw.text((170,20 ), strtime2, font = fontSize60, fill = 0)
    #显示年月日
    draw.text((34, 70), strtime, font = fontSize20, fill = 0)
    #显示城市
    #draw.text((220, 55), tempArray[0], font = fontSize16, fill = 0)
    #天气图标
    tempTypeIcon = Image.open(rootPath + "/pic/weatherType/" + UpdateWeatherIcon(tempArray[4]))
    Himage.paste(tempTypeIcon,(375,30))
    #今日天气
    draw.text((435,20),tempArray[4], font = fontSize25, fill = 0)
    #温度
    todayTemp = ReplaceLowTemp(tempArray[2])+"-"+ReplaceHeightTemp(tempArray[3]) +" 度"
    draw.text((570,55),todayTemp, font = fontSize20, fill = 0)
    #温度图标
    TempIcon = Image.open(rootPath + "/pic/temp.png")
    Himage.paste(TempIcon,(585,15))
    #显示湿度
    draw.text((680,55),"湿度: "+ tempArray[1], font = fontSize20, fill = 0)
    #湿度图标
    tmoistureIcon = Image.open(rootPath + "/pic/moisture.png")
    Himage.paste(tmoistureIcon,(695,15))
    #风力
    windTemp = tempArray[5] + tempArray[6]
    draw.text((430,55),windTemp, font = fontSize20, fill = 0)

def DrawSchedule(draw,timeUpdate):
    global scheduleDic
    for x in range(0,len(scheduleDic)):
        t = scheduleDic[x]["dateTime"]
        subjectStr = scheduleDic[x]["subjectStr"]
        #bodyStr = scheduleDic[x]["bodyStr"]
        #黑方框标记今日
        fillColor = 0
        if(int(t.day) == int(timeUpdate.strftime('%d'))):
            draw.rectangle((30, 135 + x*65, 120, 190 + x*65), fill = "black")
            fillColor = 255
        draw.text((40,144 + x*65),str(t.month) +"月"+ str(t.day)+"日", font = fontSize20, fill = fillColor)
        draw.text((40,163 + x*65),str(t.strftime('%H:%M')), font = fontSize20, fill = fillColor)
        #日程标题
        draw.text((135,145 + x*65),str(subjectStr), font = fontSize30, fill = 0)
        #draw.text((15,80 + x*100),bodyStr, font = fontSize16, fill = 0)
 
def DrawRss(draw):
    global scheduleDic
    global scheduleDic2
    global switchRss
    global nowPage
    global unitCount
    global minDicCount
    drawDic = scheduleDic
    if(switchRss):
        drawDic = scheduleDic
    else:
        drawDic = scheduleDic2
    
    if(len(drawDic) <= 1):
        draw.text((10,130),"暂无新闻源...", font = fontSize30, fill = 0)
        return

    #新闻源长度
    drawDicLen = len(drawDic)
    minDicCount += unitCount
    
    #print("--------drawDicLen: " + str(drawDicLen))
    #print("--------nowPage: " + str(nowPage))
    #print("--------minDicCount: " + str(minDicCount))
          
    if(minDicCount > drawDicLen):
        minDicCount = unitCount
    if nowPage > (drawDicLen - unitCount):
        nowPage = 0
    tempY = 0
    for x in range(nowPage,minDicCount):
        #rss标题    
        subjectStr = drawDic[min(drawDicLen-1,x)]["subjectStr"]
        draw.text((10,130 + tempY *45),str(subjectStr), font = fontSize30, fill = 0)
        tempY += 1
    nowPage += unitCount
        
 
def WeatherStrSwitch(index):
    if index == 0:
        return"明天"
    elif index == 1:
        return"后天"
    elif index == 2:
        return"大后天"

def WeatherSwitch(index):
    if index == 0:
        return 4
    elif index == 1:
        return 9
    elif index == 2:
        return 14

def DrawWeather(draw,Himage):
    for x in range(0,3):
        draw.text((580,145 + x *155),WeatherStrSwitch(x), font = fontSize20, fill = 0)
        strWeather = tempArray[WeatherSwitch(x)]
        #风力
        windTemp = tempArray[WeatherSwitch(x)+1] + tempArray[WeatherSwitch(x)+2]
        draw.text((690,145 + x *155),windTemp, font = fontSize20, fill = 0)
        #图标
        pathIcon = UpdateWeatherIcon(strWeather)
        tempTypeIcon = Image.open(rootPath + "/pic/weatherType/" + pathIcon)
        Himage.paste(tempTypeIcon,(580,180 + x*155))
        #天气
        draw.text((660,188 + x *155),strWeather, font = fontSize25, fill = 0)
        #温度
        forecastTemp = ReplaceLowTemp(tempArray[WeatherSwitch(x)-2])+"-"+ReplaceHeightTemp(tempArray[WeatherSwitch(x)-1]) +" 度"
        draw.text((650,220 + x *155),forecastTemp, font = fontSize20, fill = 0)

def ClearScreen():
    global config
    if int(config[4][1]) == 0:
        clearPathStr = rootPath.replace("\\","/") +"/black.png"
        resolution = ",w=" + config[9][1]
        fbinkBlackStr = "fbink -c -g file=" + clearPathStr + resolution + ",halign=center,valign=center"
        os.system("fbink -c")
        os.system(fbinkBlackStr)
        os.system("fbink -c")
        os.system("fbink -c")

    #时间刷新循环
def UpdateTime():
    global clearCount
    global switchRss
    global config
    oldIntTimeH = 0
    bgName = ""
    while (True):
        print(GetTime()+'Update Init...', flush=True)
        #10分钟清空一次屏幕
        clearCount += 1
        if clearCount >10:
            ClearScreen()
            clearCount = 0
        timeUpdate = DatetimeNow()
        #时间
        strtimeHM = timeUpdate.strftime('%H%M')
        #小时
        strtimeH = timeUpdate.strftime('%H')   
        intTimeH = int(strtimeH)
        #新建空白图片
        Himage = Image.new('1', (800, 600), 255)
        Himage2 = Image.new('1', (800, 600), 255)
        draw = ImageDraw.Draw(Himage)
        drawRss = ImageDraw.Draw(Himage2)
        #显示背景
        if int(config[6][1]) == 1:
            bgName = "bgRss.png"
        else:
            bgName = "bg.png"
        bmp = Image.open(rootPath + '/pic/'+ bgName)
        bmpAlpha = Image.open(rootPath + '/pic/bgRss_Alpha.png')
        
        Himage.paste(bmp,(0,0))
        #绘制水平栏
        DrawHorizontalDar(draw,Himage,timeUpdate)
        #绘制日程
        if int(config[6][1]) == 1:
            DrawRss(drawRss)
        else:
            DrawSchedule(drawRss,timeUpdate)
            
        #绘制天气预报
        DrawWeather(draw,Himage)
        Himage.paste(Himage2,bmpAlpha.getchannel("R"))
        
        #画线(x开始值，y开始值，x结束值，y结束值)
        #draw.rectangle((280, 90, 280, 290), fill = 0)
        #反向图片
        #Himage = ImageChops.invert(Himage)
        if int(config[4][1]) == 1:
            pathStr = rootPath.replace("\\","/") +"/nowTime" + str(strtimeHM) +".png"
            pathStrList.append(pathStr)
            if len(pathStrList) >1:
                try:
                    os.remove(pathStrList[0])
                except:
                    pass
                del pathStrList[0]
            i = 0
            for x in pathStrList:
                print(GetTime() +"Image Cache List "+str(i)+" : "+str(x))
                i +=1
            if int(config[5][1]) == 1:
                Himage = Himage.transpose(Image.ROTATE_270)
        else:
            pathStr = rootPath.replace("\\","/") +"/nowTime.png"
            Himage = Himage.transpose(Image.ROTATE_90)
            
        resX = int(config[9][1])
        resY = int(config[10][1])
        Himage = Himage.resize((resX,resY),resample=Image.NEAREST)
        if(int(config[11][1]) == 1):
            Himage = Himage.transpose(Image.ROTATE_180)
        Himage.save(pathStr)
        if int(config[4][1]) == 0:
            resolution = ",w=" + config[9][1]
            fbinkStr = "fbink -c -g file=" + pathStr + resolution +",halign=center,valign=center"
            os.system(fbinkStr)
        print(GetTime() + 'Update Screen...ok', flush=True)
        
        #每小时切换一次Rss源
        if(intTimeH != oldIntTimeH):
            if(switchRss):
                switchRss = False
            else:
                switchRss = True
            oldIntTimeH = intTimeH
            print(GetTime() +"切换RSS源="+ str(switchRss))
            
        #2点～6点 每小时刷新一次
        if(intTimeH >= 1 and intTimeH <= 6):
            time.sleep(3600)
        else:
            time.sleep(60)
            

        
def GetRssDic(data,dataLen):
    dataDic = OrderedDict()
    for i in range(0,dataLen):
        elemDic = OrderedDict()
        elemDic["location"] = ""
        elemDic["dateTime"] = DatetimeNow()
        elemDic["subjectStr"] = data["entries"][i]["title"]
        elemDic["bodyStr"] = ""
        dataDic[i] = elemDic
    return dataDic
    
def GetRss():
    global scheduleDic
    global scheduleDic2
    global config
    rssData = ""
    rssData2 = ""
    while(True):
        print(GetTime()+'Start Update Rss...', flush=True)
        try:
            re = requests.get(str(config[7][1]),headers = header)
            re.encoding = "utf-8"
            rssData = feedparser.parse(re.text)

            re2 = requests.get(str(config[8][1]),headers = header)
            re2.encoding = "utf-8"
            rssData2 = feedparser.parse(re2.text)
            print(GetTime()+'Update Rss ok!', flush=True)
        except Exception as e:
            print(GetTime()+'Update Rss Fail..'+ str(e), flush=True)
   
        dataLen = len(rssData["entries"])
        dataLen2 = len(rssData2["entries"])
        print(GetTime()+"RSS源长度:Rss1=" + str(dataLen) + " Rss2 ="+ str(dataLen2))
        
        scheduleDic = GetRssDic(rssData,dataLen)
        scheduleDic2 = GetRssDic(rssData2,dataLen2)
        
        timeUpdate = DatetimeNow()
        UpdateTemp(timeUpdate)
        strtime5 = timeUpdate.strftime('%H')      
        intTime = int(strtime5)
        if(intTime >= 1 and intTime <= 6): #2点～6点 每2小时刷新一次
            time.sleep(7200)
        else:
            time.sleep(3600)
            
def NetworkThreading():
    global scheduleDic
    global config
    while (True):
        timeUpdate = DatetimeNow()
        UpdateTemp(timeUpdate)
        print(GetTime() + 'Start Update Schedule...', flush=True)
        try:
            scheduleDic = GetO365(7)
            print(GetTime() + 'Update Schedule...ok', flush=True)
        except Exception as e:
            print(GetTime() + 'Update Schedule..Fail!'+ str(e), flush=True)
            elemDic = OrderedDict()
            elemDic["location"] = ""
            elemDic["dateTime"] = DatetimeNow()
            elemDic["subjectStr"] = "日程获取失败...稍后重试"
            elemDic["bodyStr"] = ""
            scheduleDic[0] = elemDic
        
        strtimeH = timeUpdate.strftime('%H')      
        intTime = int(strtimeH)
        if(intTime >= 1 and intTime <= 6):
            time.sleep(3600)
        else:
            time.sleep(int(config[3][1]))

def GetHostIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip

    #网页服务器
def HtmlServer():
    addr = GetHostIp()
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((addr, 80), handler)
    print(GetTime()+"Html Server Start..." + addr)
    httpd.serve_forever()

UpdateData()
ClearScreen()

elemDic = OrderedDict()
elemDic["location"] = ""
elemDic["dateTime"] = DatetimeNow()
elemDic["subjectStr"] = "初始化请稍等..."
elemDic["bodyStr"] = ""
scheduleDic[0] = elemDic
scheduleDic2[0] = elemDic

Himage = Image.new('1', (800, 600), 225)
if int(config[4][1]) == 1:
    serverThreading = threading.Thread(target=HtmlServer, args=())
    serverThreading.start()

timeThreading = threading.Thread(target=UpdateTime, args=())
timeThreading.start()

if int(config[6][1]) == 1:
    networkGetRss = threading.Thread(target=GetRss, args=())
    networkGetRss.start()
else:
    networkThreading = threading.Thread(target=NetworkThreading, args=())
    networkThreading.start()





