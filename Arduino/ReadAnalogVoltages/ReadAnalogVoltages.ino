/*
  ReadAnalogVoltage

  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/ReadAnalogVoltage
*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
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
  float currentBatteryInput = ((currentBattery-1.75)/5)*(10^3) ;  //10^3 converts A to mA
  
  // print out the values you read:
  Serial.println(voltageBatteryInput);
  Serial.println(voltageSupplyInput);
  Serial.println(currentBatteryInput);
}
