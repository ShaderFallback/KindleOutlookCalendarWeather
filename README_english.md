# KindleOutlookCalendarWeather
 standAlone
 

![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_01.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_03.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_00.jpg)
![image](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/image/KindleOutlookCalendar_02.jpg)

**[中文](https://github.com/ShaderFallback/KindleOutlookCalendarWeather/blob/main/README.md)**

new Added support for RSS subscription news display 
(no need to configure calendar if RSS is enabled) 
Double Rss links (switch and play two news sources every hour) 
If the number of Rss exceeds the number of single pages, turn the page once every minute

#1. Jailbreak first 
https://bookfere.com/novice#novice_8_1 
https://bookfere.com/post/892.html

#2. Install KUAL - Plugin Program Launcher 
https://bookfere.com/post/311.html#p_2

#3. Install USBNetwork Hack - Wireless Management Kindle 
(for logging in SSH, you can skip this step) 
https://bookfere.com/post/311.html#p_6

#3. Install Rename OTA binaries to disable automatic upgrade 
https://bookfere.com/post/472.html

#4. Install Kindle-specific Python3.9 
https://bookfere.com/post/311.html#p_6

(No need to configure this step if you only watch RSS) 
#5. Enable Api permissions for Outlook email, get client ID and password value (how to get it, watch this video) https://www.bilibili.com/video/BV1Sa411E7qk?spm_id_from=333.999.0.0&vd_source=5228a3ffeeee092609a234a5dbf99989

(No need to configure this step if you only watch RSS) 
#6. Use the token generation tool to generate a token file
https://github.com/ShaderFallback/KindleOutlookCalendarWeather/releases/tag/0.1

(No need to configure this step if you only watch RSS) 
#7. Put the generated o365_token.txt file in the 
KindleOutlookCalendarWeather/bin directory

(No need to configure this step if you only watch RSS) 
#8. Modify the config.ini file ClientID and ClientValue, 
it is recommended to use notepad++ and select utf8 without BOM format when saving 
Do not use Windows Notepad to edit!!! Otherwise there will be problems reading on Linux

#9. Open the city_code.json file in the scripts folder (recommend using Notepad++) 
Ctrl+F to query your city code (only China City,outher City late add~)

#10. Modify the CityCode item in the config.ini file

#11. Connect Kindle data cable to computer, copy KindleOutlookCalendarWeather folder to extensions folder

#12.Open Kual app launcher, click Outlook weather calendar menu -> WeatherCalendar_ON to start the app
Jailbreak original post link https://www.mobileread.com/forums/showthread.php?t=225030

Non-jailbreak solution You need a Windows or Linux server and install Python environment, modify the configuration file config.ini Set HtmlServer item to 1 , run script WeatherStation.py and you can directly access the web page on Kindle If you want to save money, you can also buy a domestic ARM development board like Orange Pi or a second-hand thin client

Frequently Asked Questions:
[log error] (sh: fbink: not found) Solution: Install USBNetwork Hack or you may not have the fbink command
[log error] import ImageFont ImportError: The _imagingft C module is not installed Solution: Restore the system and reinstall the
latest version of Python3. Connect to https://www.mobileread.com/forums/showthread.php?t=225030
[log error] [FBInk] [fbink_open] Cannot open framebuffer character device: Permission denied!
Use the RUNME.sh script to start it.

Bilibili 日出东水 原创制作
https://space.bilibili.com/319287192
