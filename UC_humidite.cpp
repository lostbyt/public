//=====================================//
//      Random byte generator
//        byte receiver
// 
//emmanuel Moulun
//commentaire:
//Interruption externe declenchee par 
//le capteur sur PIN2. Lecture d'un
//bit chaque seconde sur PIN3. LED en
//PIN5 s'allume lors de la Tx.
//
//====================================//

#include <Arduino.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <LiquidCrystal.h>

bool flag= false;
unsigned long startTime;
unsigned long currentTime;
const int rs = 12, en = 13, d4 = 11, d5 = 10, d6 = 9, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
#define INTERBITS 1000


/////
void setup()
{
  
  DDRD |=~(1<<2);     //External interruption pin
  DDRD |=~(1<<3);     //bits receiver
  DDRD |= (1<<5);  	  //LED tx
  PORTD &=~(1<<5);  
  
  sei();                //interrupions authorisee
  EICRA |= 0b00000011;  //interruption sur front montant
  EIMSK |= 0b00000001;  //registre des masques, INT1 on

  Serial.begin(9600);
}

/////
void byteToDec(int* toDec){
  float rawVal = 0;
  int power  = 0;
  float Percentage;
  
  for (int i=8; i>=1; i--){
    rawVal += toDec[i]*(pow(2,power));
    
    Percentage = (100 * rawVal) / 255.0;
    
	lcd.setCursor(0, 0);
  	lcd.print("Humidity:");
  	lcd.setCursor(0, 1);
  	lcd.print(Percentage, 0);
  	lcd.print(" %");
  	lcd.print("    ");
    
    power ++;
  }
  
  Serial.print("humidite:");
  Serial.print(Percentage);
  Serial.println("%");
  
}

/////
void bitsCollector(int* buffer){
  
  for (int j= 0; j<=8; j++){
    buffer[j] = bitRead(PIND,3);
    startTime = millis();
    currentTime= millis();
    
    while (currentTime - startTime < INTERBITS)
    {
      currentTime= millis();
    }
  }
  Serial.println(" ");
  byteToDec(buffer);
  flag= false;
  
  PORTD &=~(1<<5); 
}

/////
void loop()
{
  int buffer[8]= {0};
  
  if ((flag == true)){
    bitsCollector(buffer);
    EIMSK |= 0b00000001;
  }
}

///// 
ISR(INT0_vect)
{
  PORTD |=(1<<5);
  flag = true;
}