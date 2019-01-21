#!/usr/bin/env python3
import tkinter as tk 
from tkinter.font import Font
from tkinter import messagebox
from gpiozero import LED
import serial
import time
from barcode import barcode_reader
from tst import transfer_data
from controlEyes import *

import threading
from threading import Thread
import re

url = "http://xabialab.org/drautonomo/usuarios.php?orden=%20INSERT%20INTO%20`Registro`(`IdRobot`,%20`dni`,%20`Estatura`,%20`RitmoCardiaco`,%20`Peso`)%20VALUES%20({},{},{},{},{})"
arduino = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=15, stopbits=serial.STOPBITS_ONE)

led = LED(19)

def on_closing():
	global root
	global task0
	global dead
	if messagebox.askokcancel("Quit", "¿Desea cerrar la aplicación?"):
		arduino.close()
		dead = True
		root.destroy()

def gui():
	global root
	root = tk.Tk()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	app = App(root)
	app.start()
	app.mainloop()

def tasks():
	global task0
	task0 = Task()
	task0.start()

def main():
	tasks()
	gui()

class Task(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global dead
		dead = False
		while not dead:
			# arduino.write(b'w')
			# value = ''.join(c for c in str(arduino.read()) if c not in 'b\'\\r\\n')
			
			value = 0.0
			value2 = 0.0
			arduino.write(bytes('w', 'utf-8'))
			arduino.flush()
			# value = arduino.readline()
			value2 = arduino.read_until('\n') 
			# value = value.decode('utf-8')
			# value3 = value2.decode('utf-8')
			# value3 = value3.decode('utf-8')
			# value2 = value2.replace("\n","\0")
			value3 = value2
			value3 = value3.decode('utf-8')
			value4 = float(value3)
			
			# print('tipo: [{}], valor: [{}]\n'.format(type(value), value))
			print('tipo: [{}], valor: [{}]'.format(type(value4), value4))
			
			# line_data = re.findall("\d*\.\d*|\d*",str(arduino.readline())) # Find all digits
			# line_data = [float(element) for element in line_data if is_number(element)] # Convert strings to float
			# print(type(line_data))
			# print(line_data)
			
			time.sleep(1)
			# print('peso: {}'.format(str(float(arduino.readline()))))
			# eyes_green_on()
			# time.sleep(0.5)
			# eyes_green_off()
			# time.sleep(0.5)

class App(threading.Thread, tk.Frame):
	def __init__(self, master):
		threading.Thread.__init__(self)
		tk.Frame.__init__(self, master)
		self.pack()
		self.master.title("Doctor Autonoma")
		self.master.resizable(True, True)
		self.master.tk_setPalette(background='#FFFFFF')
		self.master.geometry("{}x{}".format(900, 500))
		self.master.config(menu=tk.Menu(self.master))
		dialog_frame = tk.Frame(self)
		dialog_frame.pack(padx=20, pady=15)
		tk.Label(dialog_frame, text="Presione boton Iniciar", fg='#FF8A00').pack()
		button_frame = tk.Frame(self)
		button_frame.pack()
		buttonFont = Font(family='Helvetica', size=20, weight='bold')
		
		self.varChk = tk.IntVar()
		self.chk = tk.Checkbutton(self, text='Permito uso de datos', variable=self.varChk, height=5, width = 20)
		self.chk.pack(anchor='w')
		
		self.iniciar_button = tk.Button(button_frame, text='Iniciar', fg='#AD927D', font = buttonFont, default='active', command=self.run, height = 4 , width = 10)
		self.iniciar_button.pack(side='right')
		self.refrescar_button = tk.Button(button_frame, text='Refrescar', fg='#AD927D', font = buttonFont, default='active', command=self.refresh, height = 4, width = 10)
		self.refrescar_button.pack(side='right')
		
		self.data_frame = tk.Frame(self)
		self.data_frame.pack(padx=20, pady=15)
		tk.Label(self.data_frame, text="").pack()

	def refresh(self):
		self.varChk.set(0)
		self.chk.config(state = tk.NORMAL)
		led.on()
		self.iniciar_button.configure(state='active')
		for widget in self.data_frame.winfo_children():
			widget.destroy()

	def run(self):
		if self.varChk.get() == 0:
			print('Desactivado')
		else:
			print('Activado')
			self.chk.config(state = tk.DISABLED)
			print('LED')
			eyes_green_off()
			eyes_red_on()
			self.iniciar_button.configure(state='disabled')
			led.on()
			time.sleep(1)
			led.off()
			print('Barcode - Begin')
			# code = barcode_reader()
			# num_doc = code
			num_doc = '45120100'
			
			
			if num_doc is None:
				print('Num_doc is None')
			else:
				print('Inicio de envio de datos')
				kid = {}

				num_doc = '' if num_doc is None else str(num_doc)
				
				kid["Numero Documento"] = num_doc
				
				arduino.write(b'w')
				kid["Peso"] = str(float(arduino.readline()))
				
				arduino.write(b'h')
				kid["Estatura"] = str(float(arduino.readline()))
				
				arduino.write(b'p')
				kid["Ritmo cardiaco"] = str(int(arduino.readline()))
				
				# kid["Fecha hora"] = "{}".format(now.strftime("%d-%m-%Y %H:%M:%S"))
				kid["id"] = "{}".format("1") #id = 1
				
				kid["Tipo Documento"] = 'DNI'
				
				mssg = "Tipo Documento: {}\n\rNumero Documento: {}\n\rEstatura: {}\n\rPeso: {}\n\rRitmo cardiaco: {}\n\r".format(kid["Tipo Documento"], kid["Numero Documento"], kid["Estatura"], kid["Peso"], kid["Ritmo cardiaco"])
				data_url = ''
				data_url = url.format(int(kid['id']), float(kid['Numero Documento']), float(kid['Estatura']), int(kid['Ritmo cardiaco']), float(kid["Peso"]))
				
				# print(data_url)
				
				# state = transfer_data(data_url)
				state = 1
				
				if state is None:
					print('state of transfer_data is None')
				else:
					print('Mostrar datos')
					tk.Label(self.data_frame, text=str(mssg)).pack()
				
				print('Fin de envio de datos')

			led.on()
			eyes_red_off()
			eyes_green_on()



if __name__ == '__main__':
	main()
