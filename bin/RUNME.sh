#!/bin/sh

mntroot rw


if pgrep -f "WeatherStation.py" >/dev/null; then
  echo "进程在运行中，正在关闭..."
  pkill -f "WeatherStation.py"
  fbink -x 10 -y 35 "WeatherCalendar_OFF"
  fbink -x 2 -y 38 "OpenSourceCode to:"
  fbink -x 2 -y 40 "https://Github.com/ShaderFallback"
  sleep 5
else
  echo "进程未在运行中，正在启动..."
  fbink -c -g file=/mnt/us/extensions/KindleOutlookCalendarWeather/bin/black.png,w=600,halign=center,valign=center
  sleep 1
  fbink -c
  fbink -c -g file=/mnt/us/extensions/KindleOutlookCalendarWeather/bin/logo.png,w=600,halign=center,valign=center
  nohup python3 -u /mnt/us/extensions/KindleOutlookCalendarWeather/bin/WeatherStation.py > /mnt/us/extensions/KindleOutlookCalendarWeather/bin/log.log 2>&1 &
fi

