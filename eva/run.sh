sleep 45
pkill -9 python3
sudo chmod 777 /dev/hidraw0
XAUTHORITY=/home/pi/.Xauthority DISPLAY=:0 python3 /home/pi/Desktop/eva/prod.py
