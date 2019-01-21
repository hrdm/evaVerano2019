#include <string.h>
#include "HX711.h"

#define NumSamples 4

#define calibration_factor -6350.0
#define DOUT A4
#define CLK A5
HX711 scale(DOUT,CLK);
float peso;
char peso_str[6];


#define TRIGGER 2
#define ECHO 3
#define cal_distan 180;
float altura;
char altura_str[6];
float tiempo;
float distancia;
char tmp1[6];
char tmp2[6];


int pulsePin = A0;
int pulsos;
volatile int BPM;
volatile int Signal;
volatile int IBI = 600; //tiempo entre pulsos
volatile boolean Pulse = false; //true 4 high & false 4 low
volatile boolean QS = false; //true when search 4 a pulse


float sum;
char msj[50];
char bufferEnvio[256];
char buffertmp[64];

String buffn;
void setup() {
	/*[Inicio] - Transferencia de datos*/
	Serial.begin(9600);
	/*[Fin] - Transferencia de datos*/

	/*[Inicio] - Peso*/
	scale.set_scale(calibration_factor);
	scale.tare();
	/*[Fin] - Peso*/

	/*[Inicio] - Estatura*/
	pinMode(TRIGGER, OUTPUT);
	pinMode(ECHO, INPUT);
	/*[Fin] - Estatura*/

	/*[Inicio] - Pulso*/
	/*Calibración de sensor de pulso*/
	interruptSetup();
	/*[Fin] - Pulso*/
	asm(".global _printf_float");
}

void loop() {
	if(Serial.available() > 0){
		int key = Serial.read();
		switch (key){
			case ('w'):	/*[Peso]*/
				// Serial.println("Peso");
				noInterrupts();
				peso = scale.get_units()/3.925;
				if (peso < 0) {
					peso = 0;
				}
				interrupts();
				Serial.println(peso);
				break;

			case ('h'):	/*[Estatura]*/
				// Serial.println("Estatura");
				digitalWrite(TRIGGER, LOW);
				delayMicroseconds(5);
				digitalWrite(TRIGGER, HIGH);
				delayMicroseconds (10);
				tiempo = pulseIn (ECHO, HIGH);
				distancia = int(0.017*tiempo);
				altura = cal_distan - distancia;
				altura /=100.0;
				// Serial.print("tiempo: "); Serial.println(tiempo);
				// Serial.print("distancia: "); Serial.println(distancia);
				// Serial.print("altura: "); 
				Serial.println(altura);
				break;

			case ('p'):	/*[Inicio] - Pulso*/
				// Serial.println("Pulso");
				pulsos = BPM;
				if(QS == true){
					QS = false;
				}
				Serial.println(pulsos);
				break;
		}
	}
}
