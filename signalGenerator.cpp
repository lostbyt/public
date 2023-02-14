
//=====================================//
//      Random byte generator
//        Simulate a sensor
//
//Emmmanuel Moulun
//commentaire:
//Simule un capteur d'humidite qui
//envoie un byte en 8s (1bit/s) avec
//une pause de 2s ensuite. La LED au
//PIN7 s'allume lors de la Tx.
//
//====================================//

#include <Arduino.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int i = 0, min = 0, max = 1;
unsigned  long startMillis;
unsigned  long currentMillis;
#define BREAKTIME 2000
#define INTERBITS 1000


/////
void setup()
{
  Serial.begin(9600);
  srand(time(NULL));
  DDRD |= (1<<3);               //External interrupt starter
  DDRD |= (1<<4);               //Bits sender
  DDRD |= (1<<7);               //LED tx
  startMillis = millis();
}

/////
int bitGenerator(void){
  int randomBit = (rand() % (max +1 - min)) +min;
  return randomBit;
}

/////
void loop(){
  currentMillis = millis();
  
  if (currentMillis - startMillis > BREAKTIME){
    
    for (int i=0; i<=8; i++){
      PORTD |= (1<<7);
      
      if (i==0){
        PORTD |= (1<<3);        //interrupt starter
        Serial.println("Interrupt sent");
        
      }else{
        PORTD &=~(1<<3);
        int randomBit = bitGenerator();
        Serial.print(randomBit);
        
        if (randomBit==1) {
          PORTD |= (1<<4);
          delay(INTERBITS);
        } else{
          PORTD &=~ (1<<4);
          delay(INTERBITS);
        }
      }
    }
    
    Serial.println("---end of byte");
    PORTD &=~(1<<7);
    startMillis = millis();
  } 
}
