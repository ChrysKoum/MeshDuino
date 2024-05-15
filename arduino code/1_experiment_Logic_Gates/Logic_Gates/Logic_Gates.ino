#include <RH_RF22.h>
#include <SPI.h>

// RFM22 setup
#define MY_ADDRESS 1
#define DESTINATION_ADDRESS_1 0

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

  //RX,TX

  if (!rf22.init())
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(434.0)) // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  );// The modulation should be the same as that of the transmitter. Otherwise no communication will take place
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay 




void loop() {
   //Rx code receive code from center arduino
  
  uint8_t buf[RF22_ROUTER_MAX_MESSAGE_LEN];  // Buffer to hold incoming data
  char incoming[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold converted incoming data as a string
  memset(buf, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(incoming, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  uint8_t len = sizeof(buf); // Length of the incoming data
  uint8_t from; // Variable to store the sender's address

  // Check if data is received
  if (rf22.recvfromAck(buf, &len, &from)) {
    buf[len] = '\0'; // Ensure null-termination for proper string handling
    memcpy(incoming, buf, len + 1); // Copy received data into incoming buffer, ensuring it's a valid string

    Serial.print("Message received from address: ");
    Serial.println(from, DEC); // Display the sender's address
    Serial.print("Message: ");
    Serial.println(incoming); // Display the received message as a string
    delay(1000);
} 

if(incoming=="Arduino 1 get start")
{
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

  //sent to center arduino that the experiment is finished 
      char message[] = "finish";
     uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
     memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);    
     memcpy(data_send, message, strlen(message));

   if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) {
     Serial.println("sendtoWait failed");
   }
   else {
    Serial.println("sendtoWait Successful");
   }
   delay(1000);
  

      
       // const char* msg = "Success";
      //  rf22.setHeaderTo(DESTINATION_ADDRESS_1); // Set the destination address
     //        rf22.send((uint8_t*)msg, strlen(msg));   // Send the message
     //   rf22.waitPacketSent();                   // Wait until the message is sent
      
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

 
  
  
}
