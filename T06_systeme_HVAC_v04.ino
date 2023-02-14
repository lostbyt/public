//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::://
//                                                                //
//          Programme de régulation d'un système HVAC             //
//                      Emmanuel Moulun                           //
//                          V 04                                  //
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::://




//Constantes
#define numReadings 7                  //représente le nombre de valeurs prise par le capteur pour la moyenne
#define SP_DEGRES 25                   //représente la temperature de consigne en degrés
#define chauffage1 4
#define chauffage2 5
#define refroidisseur1 2
#define refroidisseur2 3
#define limiteTresBasseVoltage 1.23   //représente la température de 10 degrés en voltage avec gain de 2
#define limiteBasseVoltage 1.41       //représente la température de 20 degrés en voltage avec gain de 2
#define limiteTresHauteVoltage 1.77   //représente la température de 40 degrés en voltage avec gain de 2
#define limiteHauteVoltage 1.59       //représente la température de 30 degrés en voltage avec gain de 2
#define alarm 8                       
#define timeAlarm 600000
#define signalFREEZY 9
#define signalOVERHEAT 10



//Variables
float lstValSensor1[numReadings]; 
float lstValSensor2[numReadings]; 
int indexSensor1          = 0;
int indexSensor2          = 0;
float totalSensor1        = 0; 
float totalSensor2        = 0; 
float averageSensor1      = 0;
float averageSensor2      = 0;
float inputSensor1        = A0;
float inputSensor2        = A1;

int globalTemperatureBITS = 0;
float PV_VOLTAGE          = 0;
float error               = 0;
unsigned long startMillis;
unsigned long currentMillis;


void setup()

{
  Serial.begin(9600);			
  for (int thisReading = 0; thisReading < numReadings; thisReading++){
    lstValSensor1[thisReading] = 0;
  }

  startMillis= millis();
  pinMode(chauffage1, OUTPUT);
  pinMode(chauffage2, OUTPUT);
  pinMode(refroidisseur1, OUTPUT);
  pinMode(refroidisseur2, OUTPUT);
  pinMode(signalFREEZY, OUTPUT);
  pinMode(signalOVERHEAT, OUTPUT);
  pinMode(alarm, OUTPUT);
}

void loop() {
  
  currentMillis= millis();

  globalTemperatureBITS= (makeAverageSensorOne()+ makeAverageSensorTwo())/2;	//Moyenne des deux capteurs
  
  //Definition de la process value, du set point et de l'erreur.
  PV_VOLTAGE= globalTemperatureBITS*(5/1023.0);
  float SP_VOLTAGE= (0.009 * SP_DEGRES + 0.525)*2; //equation lineaire a partir de la courbe de transfert du TMP36 avec gain de 2 (AO)
  error= SP_VOLTAGE - PV_VOLTAGE;
  
  if(PV_VOLTAGE>=limiteTresBasseVoltage && PV_VOLTAGE<=limiteHauteVoltage){
    cycleNormal(error);
  }else{
    if(PV_VOLTAGE<limiteTresBasseVoltage){
      cycleFreezyVeryLow(PV_VOLTAGE);
    }else{
      if(PV_VOLTAGE<limiteBasseVoltage){
        cycleFreezy(PV_VOLTAGE);
      }else{
        if(PV_VOLTAGE>limiteTresHauteVoltage){
          cycleVeryOverheat(PV_VOLTAGE);
        }else{
          if(PV_VOLTAGE>limiteHauteVoltage){
            cycleOverheat(PV_VOLTAGE);
          }
        }
      }
    }
  }
  
  
  //PRINTS
  Serial.print("Temperature moyenne: ");
  float tmp= ((PV_VOLTAGE/2)-0.525);
  Serial.println(tmp/0.009);
  Serial.print("Erreur: ");
  Serial.println(error);
}


float makeAverageSensorOne(){
  totalSensor1-= lstValSensor1[indexSensor1]; // subtract the last reading
  
  lstValSensor1[indexSensor1] = analogRead(inputSensor1);
  totalSensor1+= lstValSensor1[indexSensor1];
  indexSensor1 ++;
  
  if (indexSensor1 >= numReadings)
    indexSensor1 = 0;
  
  averageSensor1 = (totalSensor1 / numReadings);
  delay(1);
  
  return averageSensor1;
}


float makeAverageSensorTwo(){
  totalSensor2-= lstValSensor2[indexSensor2]; // subtract the last reading
  
  lstValSensor2[indexSensor2] = analogRead(inputSensor2);
  totalSensor2+= lstValSensor2[indexSensor2];
  indexSensor2 ++;
  
  if (indexSensor2 >= numReadings)
    indexSensor2 = 0;
  
  averageSensor2 = (totalSensor2 / numReadings);
  delay(1);
  
  return averageSensor2;
}


void cycleNormal(float error){
  startMillis= millis();    //necessaire aussi dans le cycle normal afin de garder une reference de temps

  if (error>0.04){
    digitalWrite(chauffage1, HIGH);
    digitalWrite(chauffage2, LOW);
    digitalWrite(refroidisseur1, LOW);
    digitalWrite(refroidisseur2, LOW);
    digitalWrite(signalFREEZY, LOW);
    digitalWrite(signalOVERHEAT, LOW);
    digitalWrite(alarm, LOW);
  }else{
    if (error<-0.04){
      digitalWrite(chauffage1, LOW);
      digitalWrite(chauffage2, LOW);
      digitalWrite(refroidisseur1, HIGH);
      digitalWrite(refroidisseur2, LOW);
      digitalWrite(signalFREEZY, LOW);
      digitalWrite(signalOVERHEAT, LOW);
      digitalWrite(alarm, LOW);
    }else{
      digitalWrite(chauffage1, LOW);
      digitalWrite(chauffage2, LOW);
      digitalWrite(refroidisseur1, LOW);
      digitalWrite(refroidisseur2, LOW);
      digitalWrite(signalFREEZY, LOW);
      digitalWrite(signalOVERHEAT, LOW);
      digitalWrite(alarm, LOW);
    }
  }
}


void cycleFreezyVeryLow(float PV_VOLTAGE){
  if ((currentMillis - startMillis) > timeAlarm){
    digitalWrite(alarm, HIGH);
    startMillis= millis();
  }
  
  if (PV_VOLTAGE<1.52){
    digitalWrite(signalFREEZY, HIGH);
    digitalWrite(chauffage1, HIGH);
    digitalWrite(chauffage2, HIGH);
    digitalWrite(refroidisseur1, LOW);
  }else{
    digitalWrite(signalFREEZY, LOW);
    digitalWrite(chauffage2, LOW);
  }
}


void cycleFreezy(float PV_VOLTAGE){
  if ((currentMillis - startMillis) > timeAlarm){
    digitalWrite(alarm, HIGH);
    startMillis= millis();
  }
  
  if (PV_VOLTAGE<1.4){
    digitalWrite(signalFREEZY, LOW);
    digitalWrite(chauffage1, HIGH);
    digitalWrite(chauffage2, LOW);
    digitalWrite(refroidisseur1, LOW);
  }else{
    digitalWrite(signalFREEZY, LOW);
    digitalWrite(chauffage2, LOW);
  }
}


void cycleOverheat(float PV_VOLTAGE){
  if ((currentMillis - startMillis) > timeAlarm){
    digitalWrite(alarm, HIGH);
    startMillis= millis();
  }
  
  if (PV_VOLTAGE>1.614){
    digitalWrite(signalOVERHEAT, LOW);
    digitalWrite(chauffage1, LOW);
    digitalWrite(chauffage2, LOW);
    digitalWrite(refroidisseur1, HIGH);
    digitalWrite(refroidisseur2, LOW);
  }else{
    digitalWrite(signalOVERHEAT, LOW);
    digitalWrite(refroidisseur2, LOW);
  }
}


void cycleVeryOverheat(float PV_VOLTAGE){
  if ((currentMillis - startMillis) > timeAlarm){
    digitalWrite(alarm, HIGH);
    startMillis= millis();
  }
  
  if (PV_VOLTAGE>1.614){
    digitalWrite(signalOVERHEAT, HIGH);
    digitalWrite(chauffage1, LOW);
    digitalWrite(chauffage2, LOW);
    digitalWrite(refroidisseur1, HIGH);
    digitalWrite(refroidisseur2, HIGH);
  }else{
    digitalWrite(signalOVERHEAT, LOW);
    digitalWrite(refroidisseur2, LOW);
  }
}