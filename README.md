# KindleOutlookCalendarWeather
 standAlone
 

![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_01.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_03.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_00.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_02.jpg)

**[English](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/README_english.md)**

new 新增支持RSS 订阅新闻显示(如果启用RSS,无需配置日历)
双Rss链接(每小时切换轮播两个新闻源)
如果Rss数量超过单页数量,每分钟翻页一次
 
#1.先越狱
https://bookfere.com/novice#novice_8_1
https://bookfere.com/post/892.html

#2.安装 KUAL — 插件程序启动器
https://bookfere.com/post/311.html#p_2

#3.安装 USBNetwork Hack – 无线管理 Kindle （用于登录SSH 可以不装）
https://bookfere.com/post/311.html#p_6

#3.安装 Rename OTA binaries 禁止自动升级 
https://bookfere.com/post/472.html

#4.安装Kindle 专用 Python3.9
https://bookfere.com/post/311.html#p_6

令牌生成步骤 (只看RSS无需配置此步骤)
1.第一步注册应用
https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2.身份验证，添加重定向 网址
https://login.microsoftonline.com/common/oauth2/nativeclient 
3.记下应用程序（客户端）ID 和 密码值

(只看RSS无需配置此步骤)
#5. 开通Outlook邮箱的Api权限, 得到客户端ID 和 密码值 (如何获取看这个视频)
https://www.bilibili.com/video/BV1Sa411E7qk?spm_id_from=333.999.0.0&vd_source=5228a3ffeeee092609a234a5dbf99989

(只看RSS无需配置此步骤)
#6. 使用令牌生成工具,生成令牌文件 https://github.com/ShaderFallback/KindleOutlookCalendarWeather/releases/tag/0.1

(只看RSS无需配置此步骤)
#7. 将生成好的 o365_token.txt 文件放在 KindleOutlookCalendarWeather/bin  目录下

(只看RSS无需配置此步骤)
#8. 修改 config.ini 文件 ClientID 和 ClientValue,推荐使用notepad++ 保存时选择 utf8无BOM格式
不能使用Windows记事本编辑!!!,否则在Linux上读取会出问题

#9. 打开scripts文件夹下的 city_code.json(建议用Notepad++) Ctrl+F 查询你所在的城市代码

#10. 修改 config.ini 文件CityCode 项

#11. Kindle数据线连接电脑, 将KindleOutlookCalendarWeather 文件夹拷贝到extensions 文件夹下

#12.打开 Kual 应用启动器, 点击Outlook天气台历菜单 -> WeatherCalendar_ON  启动应用


越狱原贴链接
https://www.mobileread.com/forums/showthread.php?t=225030

非越狱方案
你需要有一个 Windows  或 Linux 服务器并安装Python环境, 修改配置文件 config.ini 
中 HtmlServer 项设置为 1 , 运行脚本WeatherStation.py 即可在Kindle 上直接访问网页
如果想省钱也可以购买一个 香橙派之类的国产ARM开发板,或二手的瘦客户机


Bilibili 日出东水 原创制作
https://space.bilibili.com/319287192
