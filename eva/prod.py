#!/usr/bin/env python3
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
from gpiozero import LED
import json
import requests
import yaml
import serial
import time
import sys
import os
from barcode import barcode_reader#, barcode_reader_close
from transfer import *
import datetime
from tst import transfer_data
from controlEyes import *

url = "http://xabialab.org/drautonomo/usuarios.php?orden=%20INSERT%20INTO%20`Registro`(`IdRobot`,%20`dni`,%20`Estatura`,%20`RitmoCardiaco`,%20`Peso`)%20VALUES%20({},{},{},{},{})"

data_url = ''

id = "1"
localdir = '/home/pi/Desktop/drrobot/files'

arduino = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=15, stopbits=serial.STOPBITS_ONE)

time.sleep(2)
arduino.flush()
timeout = 5
t = 0
led = LED(19)
led.on()
now = datetime.datetime.now()
struct = {}
query = "INSERT INTO Registros('IdRobot', 'TipoDocumento', 'NumeroDocumento', 'Estatura', 'RitmoCardiaco', 'Peso', 'IndiceGrasaCorporal', 'FechaHora') VALUES ({}, {}, {}, {}, {}, {}, {}, {})"
SIM800L_RST = LED(16)
class App(tk.Frame):
	def __init__(self, master):
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
		
		
		global varChk
		varChk = tk.IntVar()
		# self.selection.set('white')
		
		global chk
		# tk.Radiobutton(self, text='Permitir guardar datos', value='blue', variable=self.selection, command=self.set_color).pack(anchor='w')
		chk = tk.Checkbutton(self, text='Permito uso de datos', variable=varChk, height=5, width = 20)
		chk.pack(anchor='w')
		
		global iniciar_button
		global refrescar_button
		
		iniciar_button = tk.Button(button_frame, text='Iniciar', fg='#AD927D', font = buttonFont, default='active', command=self.iniciar, height = 4 , width = 10)
		iniciar_button.pack(side='right')
		refrescar_button = tk.Button(button_frame, text='Refrescar', fg='#AD927D', font = buttonFont, default='active', command=self.refrescar, height = 4, width = 10)
		refrescar_button.pack(side='right')
		
		global data_frame
		data_frame = tk.Frame(self)
		data_frame.pack(padx=20, pady=15)
		tk.Label(data_frame, text="").pack()

	def iniciar(self):
		if varChk.get() == 0:
			print('Desactivado')
		else:
			print('Activado')
			chk.config(state = tk.DISABLED)
			print('LED')
			eyes_green_off()
			eyes_red_on()
			iniciar_button.configure(state='disabled')
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

				num_doc = xstr(num_doc)
				kid["Numero Documento"] = ''
				kid["Numero Documento"] = num_doc
				arduino.write(b'w')
				kid["Peso"] = str(float(arduino.readline()))
				arduino.write(b'h')
				kid["Estatura"] = str(float(arduino.readline()))
				arduino.write(b'p')
				kid["Ritmo cardiaco"] = str(int(arduino.readline()))
				kid["Fecha hora"] = "{}".format(now.strftime("%d-%m-%Y %H:%M:%S"))
				kid["id"] = "{}".format(id)
				kid["Tipo Documento"] = 'DNI'
				mssg = "Tipo Documento: {}\n\rNumero Documento: {}\n\rEstatura: {}\n\rPeso: {}\n\rRitmo cardiaco: {}\n\r".format(kid["Tipo Documento"], kid["Numero Documento"], kid["Estatura"], kid["Peso"], kid["Ritmo cardiaco"])

				# data_url = url.format(kid['id'], kid['Tipo Documento'], kid['Estatura'], kid['Ritmo cardiaco'], kid['Peso'])
				data_url = url.format(int(kid['id']), float(kid['Numero Documento']), float(kid['Estatura']), int(kid['Ritmo cardiaco']), float(kid["Peso"]))
				print(data_url)
				state = transfer_data(data_url)
				# requests.session().close()
				if state is None:
					print('state of transfer_data is None')
				else:
					print('Mostrar datos')
					tk.Label(data_frame, text=str(mssg)).pack()
				
				print('Fin de envio de datos')
				# arduino.write(b'a')
				# raw_data = arduino.readline()
				# print('raw_data: {} type {}'.format(raw_data, type(raw_data)))
				# kid = yaml.load(raw_data)
				
				# num_doc = xstr(num_doc)
				# print('Prueba')
				# print(num_doc)
				# kid["Numero Documento"] = ''
				# kid["Numero Documento"] = num_doc
				
				# kid["Fecha hora"] = "{}".format(now.strftime("%d-%m-%Y %H:%M:%S"))
				# kid["id"] = "{}".format(id)
				
				##mssg = "Tipo Documento: {}\n\rNumero Documento: {}\n\rEstatura: {}\n\rPeso: {}\n\rRitmo cardiaco: {}\n\rDignostico: {}\n\r".format(kid["Tipo Documento"], kid["Numero Documento"], kid["Estatura"], kid["Peso"], kid["Ritmo cardiaco"], kid["Indice de grasa corporal"])
				# mssg = "Tipo Documento: {}\n\rNumero Documento: {}\n\rEstatura: {}\n\rPeso: {}\n\rRitmo cardiaco: {}\n\r".format(kid["Tipo Documento"], kid["Numero Documento"], kid["Estatura"], kid["Peso"], kid["Ritmo cardiaco"])
				
				# new_line = query.format(kid["id"], kid["Tipo Documento"], kid["Numero Documento"], kid["Estatura"], kid["Ritmo cardiaco"], kid["Peso"], kid["Indice de grasa corporal"], kid["Fecha hora"])
				
				##data_url = url.format(kid['id'], kid['Tipo Documento'], kid['Estatura'], kid['Ritmo cardiaco'], kid['Peso'])
				# data_url = url.format(int(kid['id']), float(kid['Numero Documento']), float(kid['Estatura']), int(kid['Ritmo cardiaco']), float(kid["Peso"]))
				
				# print("Subiendo datos")
				##res = requests.get(data_url)
				# transfer_data()
				##res = requests.get('http://xabialab.org/drautonomo/usuarios.php?orden= INSERT INTO `Registro`(`IdRobot`, `dni`, `Estatura`, `RitmoCardiaco`, `Peso`) VALUES (1,25364555,1.77,33,37.3)')
				# print("Datos subidos")
				# requests.session().close()
				# print("close")
				
				# tk.Label(data_frame, text=str(mssg)).pack()
				# print('En pantalla ')
				
			led.on()
			eyes_red_off()
			eyes_green_on()

	def refrescar(self):
		varChk.set(0)
		chk.config(state = tk.NORMAL)
		led.on()
		iniciar_button.configure(state='active')
		for widget in data_frame.winfo_children():
			widget.destroy()
	
def on_closing():
	if messagebox.askokcancel("Quit", "¿Desea cerrar la aplicación?"):
		arduino.close()
		root.destroy()

def xstr(s):
    return '' if s is None else str(s)

if __name__ == '__main__':
	root = tk.Tk()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	app = App(root)
	app.mainloop()

