#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 2 // define my unique address
#define DESTINATION_ADDRESS_1 0 // define who I can talk to


// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS


const int PHOTO_RESISTOR2_PIN=A1;
const int PHOTO_RESISTOR1_PIN=A0;
const int TRIG_PIN_RIGHT=7;
const int ECHO_PIN_RIGHT=6;
const int TRIG_PIN_LEFT=5;
const int ECHO_PIN_LEFT=4;
int number_of_bytes=0;

float duration_right,duration_left,distance_right,distance_left;

 int lightValue2=0;
int lightValue1=0;

void sendMessage(const char* message);
String receiveMessage();

void setup() {

  pinMode(TRIG_PIN_RIGHT, OUTPUT);
  pinMode(ECHO_PIN_RIGHT, INPUT);
  
  pinMode(TRIG_PIN_LEFT, OUTPUT);
  pinMode(ECHO_PIN_LEFT, INPUT);
  
  pinMode(PHOTO_RESISTOR1_PIN, INPUT); // Configure force sensor pin as input
  
  pinMode(PHOTO_RESISTOR1_PIN, INPUT); // Configure photoresistor pin as input
  
    Serial.begin(9600);
 
//Tx,Rx code 
 
if (!rf22.init())
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(442.0)) // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  );// The modulation should be the same as that of the transmitter. Otherwise no communication will take place
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1);

   Serial.println("set up complete");
 
}



void loop() {

 String receivedMessage = receiveMessage();


  if(receivedMessage=="Experiment 2 Start")
{
while(true)
{

 //for the right 
  digitalWrite(TRIG_PIN_RIGHT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN_RIGHT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN_RIGHT, LOW);
  
  duration_right = pulseIn(ECHO_PIN_RIGHT, HIGH);
  distance_right = (duration_right*.0343)/2;
 // Serial.print("Distance: ");
  //Serial.println(distance);
  //delay(100);
  
  
  //for the left
  digitalWrite(TRIG_PIN_LEFT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN_LEFT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN_LEFT, LOW);
  
  duration_left = pulseIn(ECHO_PIN_LEFT, HIGH);
  distance_left = (duration_left*.0343)/2;
  //Serial.print("Distance: ");
  //Serial.println(distance);
 // delay(100);

  lightValue1 = analogRead(PHOTO_RESISTOR1_PIN);
  lightValue2 = analogRead(PHOTO_RESISTOR2_PIN);



String   finishMessage = receiveMessage();

   if(finishMessage=="Experiment 2 Finish")
        {  Serial.println("Experiment 2 Finish");
          while(true){



          }
        } 
 

if (distance_right < 10) {
    // Move right
    Serial.println("Moving Right");
    Serial.print(distance_right);
    sendMessage("Right");
    delay(1500);
  } else if (distance_left < 10) {
    // Move left
    Serial.println("Moving Left");
    Serial.print(distance_left);
    sendMessage("Left");
    delay(1500);
  } else if (lightValue2 < 150) {
    // Move down
    Serial.println("Moving Down");
    sendMessage("Down");
    Serial.println(lightValue2);
    delay(1500);
  } else if (lightValue1 < 150) {
    // Move up
    Serial.println("Moving Up");
    sendMessage("Up");
    Serial.println(lightValue1);
    delay(1500);
  } else {
    // If none of the conditions are met
    Serial.println("No move");
    sendMessage("No move");
    // Add your code for no movement here
    delay(1500);
  }
  
  


}//end if


}//end while

}//loop


void sendMessage(const char* message) {
 /*uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memcpy(data_send, message, strlen(message));

  if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) {
    Serial.println("sendtoWait failed");
  } else {
    Serial.println("sendtoWait Successful");
  }
  
 
 */ 
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memcpy(data_send, message, strlen(message));
    
    Serial.println("Attempting to send the movement...");

    bool success = false;
    for (int attempt = 0; attempt < 3; attempt++) {  // Retry up to 3 times
        Serial.print("Attempt ");
        Serial.println(attempt + 1);
        if (rf22.sendtoWait(data_send, strlen(message),DESTINATION_ADDRESS_1) == RF22_ROUTER_ERROR_NONE) {
            Serial.println("sendtoWait Successful");
            success = true;
            number_of_bytes+=sizeof(data_send); // I'm counting the number of bytes of my message
            Serial.print("Number of Bytes= ");
            Serial.println(number_of_bytes);//
            break;
        } else {
                   
              Serial.println("sendtoWait failed");
        }
        delay(1000); // Wait 1 second before retrying
    }
            
    if (!success) {
        Serial.println("Failed to send finish message after 3 attempts.");
        Serial.println("Experiment 2 Finish");
        
        while(true){
          
        

        }
    }


}



String receiveMessage() {
    uint8_t buf[RF22_ROUTER_MAX_MESSAGE_LEN];
    char incoming[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(buf, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memset(incoming, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    uint8_t len = sizeof(buf);
    uint8_t from;

    if (rf22.recvfromAck(buf, &len, &from)) {
        buf[len] = '\0';
        memcpy(incoming, buf, len + 1);

        Serial.print("Message received from address: ");
        Serial.println(from, DEC);
        Serial.print("Message: ");
        Serial.println(incoming);

        return String(incoming);
    }
    return "";
}



