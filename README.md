Features:

-Json to get last Pins status.<br>
-Nice responsive UI using Bootstrap.<br>

Basic instructions:

1 - Flash the micropython firmware following this link: https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html <br>
2 - Configure the wifi settings of board following: https://docs.micropython.org/en/latest/esp8266/quickref.html <br>
3 - Set I/O Pins configurations of your board in main.py<br>
4 - Move main.py to your board using webrepl or adafruit-ampy.<br>
<code>pip install adafruit-ampy</code><br>
<code>ampy -p /dev/ttyUSB0 -b 115200 put main.py main.py</code><br>
See: https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy<br>
5 - Reboot the board and acess http://esp_ip_adress to view UI and turn on and off I/O Pins.<br>

<b>Screenshots:<b><br>
  <br>
Mobile
  ![alt text](https://raw.githubusercontent.com/Henrique-Miranda/SmartHouse/master/img/smarthousemobile.jpeg "Mobile")

<br>
  
Desktop
  ![alt text](https://raw.githubusercontent.com/Henrique-Miranda/SmartHouse/master/img/smarthousedesktop.jpeg "Desktop")
