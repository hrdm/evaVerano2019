import serial
import time
import signal
from contextlib import contextmanager

# def transfer_data():
SIM800L = serial.Serial(port = "/dev/ttyUSB1", baudrate=19200, bytesize=8, timeout=15, stopbits=serial.STOPBITS_ONE)

#time.sleep(5)
SIM800L.flush()

@contextmanager
def timeout(time):
	# Register a function to raise a TimeoutError on the signal.
	signal.signal(signal.SIGALRM, raise_timeout)
	# Schedule the signal to be sent after ``time``.
	signal.alarm(time)

	try:
		yield
	except TimeoutError:
		pass
	finally:
		# Unregister the signal so it won't be triggered
		# if the timeout is not reached.
		signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
	raise TimeoutError



# custom_url = 'http://xabialab.org/drautonomo/usuarios.php?orden=%20INSERT%20INTO%20`Registro`(`IdRobot`,%20`dni`,%20`Estatura`,%20`RitmoCardiaco`,%20`Peso`)%20VALUES%20(1,45101102,1.75,75,53)'

def transfer_data(url):
	with timeout(20):
		SIM800L.flush()
		print('1')
		SIM800L.write(('AT\r').encode())
		rcv = SIM800L.readline()
		print(rcv)

		localtime = time.asctime( time.localtime(time.time()) )
		print ("Inicio :", localtime)
		print('2')
		SIM800L.write(('AT+SAPBR=3,1,"Contype","GPRS"\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)
		
		# print('2.0')
		# SIM800L.write(('AT+SAPBR=3,1,"APN","movistar.pe"\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('2.1')
		# SIM800L.write(('AT+SAPBR=3,1,"USER","movistar@datos"\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('2.2')
		# SIM800L.write(('AT+SAPBR=3,1,"PWD","movistar"\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('2.3')
		# SIM800L.write(('AT+SAPBR=1,1\r').encode())
		# SIM800L.write(('AT\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		print('3')
		SIM800L.write(('AT+SAPBR=2,1\r').encode())
		SIM800L.write(('AT\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('4')
		SIM800L.write(('AT+HTTPINIT\r').encode())
		SIM800L.write(('AT\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('5')
		SIM800L.write(('AT+HTTPPARA="CID",1\r').encode())
		SIM800L.write(('AT\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('6')
		# SIM800L.write(('AT+HTTPPARA="URL","http://xabialab.org/drautonomo/usuarios.php?orden=%20INSERT%20INTO%20`Registro`(`IdRobot`,%20`dni`,%20`Estatura`,%20`RitmoCardiaco`,%20`Peso`)%20VALUES%20(1,45101102,1.75,75,53)"\r').encode())
		SIM800L.write(('AT+HTTPPARA="URL","{}"\r'.format(url)).encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('7')
		SIM800L.write(('AT+HTTPACTION=0\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('8')
		SIM800L.write(('AT+HTTPREAD\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('9')
		SIM800L.write(('AT+HTTPTERM\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		print('10')
		SIM800L.write(('AT+SAPBR=0,1\r').encode())
		rcv = SIM800L.read(10)
		print(rcv)

		# SIM800L.close()
		localtime = time.asctime( time.localtime(time.time()) )
		print ("Fin :", localtime)
		return True
# transfer_data(custom_url)


# def transfer_data(url):
	# with timeout(20):
		# SIM800L.flush()
		# print('1')
		# SIM800L.write(('AT\r').encode())
		# rcv = SIM800L.readline()
		# print(rcv)

		# localtime = time.asctime( time.localtime(time.time()) )
		# print ("Inicio :", localtime)
		# print('2')
		# SIM800L.write(('AT+SAPBR=3,1,"APN","CMNET"\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('3')
		# SIM800L.write(('AT+SAPBR=1,1\r').encode())
		# SIM800L.write(('AT\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('4')
		# SIM800L.write(('AT+HTTPINIT\r').encode())
		# SIM800L.write(('AT\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('5')
		# SIM800L.write(('AT+HTTPPARA="CID",1\r').encode())
		# SIM800L.write(('AT\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('6')
		# SIM800L.write(('AT+HTTPPARA="URL","{}"\r'.format(url)).encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('7')
		# SIM800L.write(('AT+HTTPACTION=0\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('8')
		# SIM800L.write(('AT+HTTPREAD\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('9')
		# SIM800L.write(('AT+HTTPTERM\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# print('10')
		# SIM800L.write(('AT+SAPBR=0,1\r').encode())
		# rcv = SIM800L.read(10)
		# print(rcv)

		# localtime = time.asctime( time.localtime(time.time()) )
		# print ("Fin :", localtime)
		# return True
