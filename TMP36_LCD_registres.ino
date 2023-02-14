#include <Arduino.h>
#include <math.h>
#include <LiquidCrystal.h>


const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
float temperature;


ISR(ADC_vect){
  unsigned short int ADCbitsOutput= ADC;
  float ADCvoltOutput= ADCbitsOutput * 0.00488;
  temperature= (ADCvoltOutput - 0.52)/0.0096;
  
  lcd.setCursor(0, 0);
  lcd.print("temperature:");
  lcd.print(temperature);

  ADCSRA |= (1<<6);
}

int main(void){
  lcd.setCursor(0,0);
  
  DDRD |= B11111111;          //port d 0 to 7 set as output
  DDRB |= B00000011;          // port 8, 9 set as output
  DDRC &=~(1<<0);	          //A0 set as input

  ADCSRA |= (1<<7);           //Enable ADC
  ADCSRA |= B00000111;        //clock speed set up
  ADCSRA |= B00001000;        //enable ADC interruptions
  
  ADMUX = B01000000;          //Vref voltage use, justify right and input adc set up
  
  sei();			          //authorize interruptions

  while(true){
     ADCSRA |= (1<<6);         //start ADC conversion 
  }
}
