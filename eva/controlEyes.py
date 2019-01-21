import time
from gpiozero import LED

eyes_red = LED(26)
eyes_green = LED(20)

def eyes_green_on():
	eyes_green.on()

def eyes_red_on():
	eyes_red.on()

def eyes_green_off():
	eyes_green.off()

def eyes_red_off():
	eyes_red.off()
	
	

# for x in range(0,1,1):
	# eyes_green_on()
	# eyes_red_off()
	# time.sleep(0.5)
	# eyes_green_off()
	# eyes_red_on()
	# time.sleep(0.5)
	# eyes_green_on()
	# eyes_red_off()
	# time.sleep(0.5)
	# eyes_green_off()
	# eyes_red_on()
	# time.sleep(0.5)
# eyes_red_off()