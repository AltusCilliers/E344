bool Overcharge = false;
int PWM=252;
int PWMVary=252;
bool manualPWM = true;
int ADCValueLight_Old=0;
int ADCValueLight;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  //Setup Pin A0 as Output Pin
  pinMode(A0, OUTPUT);
  pinMode(11,OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  //Check for Overcharge Protection 
   if (Serial.available()) {
    String UserInput = Serial.readStringUntil('\n');
    UserInput.trim();

    if(UserInput.equals("OV1")){
      Overcharge = true;
      //set Pin 0 High
      digitalWrite(A0, HIGH);
    } else if (UserInput.equals("OV0")){
      Overcharge = false;
      //set Pin 0 Low
      digitalWrite(A0, LOW);
    }

    if((UserInput!="OV1")&&(UserInput!="manual")){
      PWM = UserInput.toInt()*2.52;
    } else if ((UserInput!="OV0")&&(UserInput!="manual")){
      PWM = UserInput.toInt()*2.52;
    }

   if(UserInput.equals("manual")){
      manualPWM=true;
      PWM = UserInput.toInt()*2.52;
    } else if (UserInput.equals("automatic")){
      manualPWM=false;
    }

     
   }


if(ADCValueLight<ADCValueLight_Old-5||ADCValueLight>ADCValueLight_Old+5)
{
  PWMVary = ADCValueLight/4;
}


 
if(manualPWM==true){
  analogWrite(11,PWM);
  
}
if(manualPWM==false){
  analogWrite(11,PWMVary);
 
}    
  
  // read the Battery Voltage on analog pin 1:
  int ADCValueBattery = analogRead(A1);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltageBattery = ADCValueBattery * (5.0 / 1023.0);
  // Convert the output voltage to the Original Battery Voltage
  float voltageBatteryInput = (voltageBattery+12.375)/2.25 ;

  // read the Supply Voltage on analog pin 2:
  int ADCValueSupply = analogRead(A2);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltageSupply = ADCValueSupply * (5.0 / 1023.0);
  // Convert the output voltage to the Original Battery Voltage
  float voltageSupplyInput = (voltageSupply*22)/4.5 ;

  // read the Battery Current on analog pin 9:
  int ADCValueCurrent = analogRead(A9);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float currentBattery = ADCValueCurrent * (5.0 / 1023.0);
  // Convert the output voltage to the Original Battery Voltage
  float currentBatteryInput = ((currentBattery-1.79)/5)*(1000) ;  //10^3 converts A to mA

  // read the Light Level on analog pin 10:
  ADCValueLight = analogRead(A10);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltageLight = ADCValueLight * (5.0 / 1023.0);
  //Convert the output voltage to a scale of 0-100%
  byte LightPercentage = (((voltageLight*0.2)-1)*-1)*100;
  
  // print out the values you read:
  Serial.print(Overcharge);
  Serial.print(", ");
  Serial.print(voltageBatteryInput);
  Serial.print(", ");
  Serial.print(voltageSupplyInput);
  Serial.print(", ");
  Serial.print(currentBatteryInput);
  Serial.print(", ");
  Serial.print(LightPercentage);
  Serial.print(", ");
  Serial.print(PWM); 
  Serial.print(", ");
  Serial.println(PWMVary);
  delay(100);
}
