#!/bin/sh
#cd "$(dirname "$0")"
#cd /mnt/us/extensions/KindleOutlookCalendarWeather/bin/
mntroot rw

fbink -c -g file=/mnt/us/extensions/KindleOutlookCalendarWeather/bin/black.png,w=600,halign=center,valign=center
sleep 1
fbink -c
fbink -c -g file=/mnt/us/extensions/KindleOutlookCalendarWeather/bin/logo.png,w=600,halign=center,valign=center
nohup python3 -u /mnt/us/extensions/KindleOutlookCalendarWeather/bin/WeatherStation.py > /mnt/us/extensions/KindleOutlookCalendarWeather/bin/log.log 2>&1 &