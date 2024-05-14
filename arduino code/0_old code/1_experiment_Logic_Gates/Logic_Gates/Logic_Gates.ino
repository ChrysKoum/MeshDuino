#include <RH_RF22.h>
#include <SPI.h>

// RFM22 setup
#define MY_ADDRESS 2
#define DESTINATION_ADDRESS_1 1

RH_RF22 rf22(MY_ADDRESS);

// constants won't change. They're used here to set pin numbers:
const int button1Pin = 2;     // the number of the pushbutton pin
const int button2Pin = 3;     // the number of the pushbutton pin

const int OutputLedPin =  13;      // the number of the Output LED pin

const int NotGate=4;  const int OrGate=5;  const int AndGate=6;
const int NorGate=7;  const int NandGate=8; const int XorGate=9;  
const int XnorGate=10;

// variables will change:
int button1State = 0;         // variable for reading the pushbutton status
int button2State = 0;
int GateSelected =4;          // not gate selected by default

void setup() {
  Serial.begin(9600);
  // initialize the LED pin as an output:
  pinMode(OutputLedPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  for(int i=4;i<=10;i++)
    pinMode(i,OUTPUT);
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);
  GateSelected=(analogRead(A0)/150)+4;
  digitalWrite(GateSelected,HIGH);
  if (!rf22.init()) {
    Serial.println("RF22 init failed");
  }
  // Set the frequency
  rf22.setFrequency(434.0);
  // Optionally set the transmission power (check RFM22 documentation for values)
  rf22.setTxPower(14);
}

void loop() {
  for(int i=4;i<=10;i++)
    digitalWrite(i,LOW);
  int vc=analogRead(A0);  
  GateSelected=(vc/150)+4;
  Serial.println(GateSelected);
  digitalWrite(GateSelected,HIGH);

  // read the state of the pushbutton value:
  button1State = digitalRead(button1Pin);
  button2State = digitalRead(button2Pin);
  
  // check the gate selected and perform action accordingly:
  if (GateSelected==NotGate){
    if(button1State==HIGH) digitalWrite(OutputLedPin,LOW); else digitalWrite(OutputLedPin,HIGH);
  }else if (GateSelected==OrGate){
    if(button1State==HIGH || button2State==HIGH) digitalWrite(OutputLedPin,HIGH); else digitalWrite(OutputLedPin,LOW);
  }else if (GateSelected==AndGate){
    if(button1State==HIGH && button2State==HIGH) {
      digitalWrite(OutputLedPin,HIGH);
        const char* msg = "Success";
        rf22.setHeaderTo(DESTINATION_ADDRESS_1); // Set the destination address
        rf22.send((uint8_t*)msg, strlen(msg));   // Send the message
        rf22.waitPacketSent();                   // Wait until the message is sent
      
      } else digitalWrite(OutputLedPin,LOW);
  }else if (GateSelected==NorGate){
    if(button1State==HIGH || button2State==HIGH) digitalWrite(OutputLedPin,LOW); else digitalWrite(OutputLedPin,HIGH);
  }else if (GateSelected==NandGate){
    if(button1State==HIGH && button2State==HIGH) digitalWrite(OutputLedPin,LOW); else digitalWrite(OutputLedPin,HIGH);
  }else if (GateSelected==XorGate){
    if(button1State==button2State) digitalWrite(OutputLedPin,LOW); else digitalWrite(OutputLedPin,HIGH);
  }else if (GateSelected==XnorGate){
    if(button1State==button2State) digitalWrite(OutputLedPin,HIGH); else digitalWrite(OutputLedPin,LOW);
  }
}
