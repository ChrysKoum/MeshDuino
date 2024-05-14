#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 0 // define my unique address
#define DESTINATION_ADDRESS_1 1 // define who I can talk to
#define DESTINATION_ADDRESS_2 2 // define who I can talk to
#define DESTINATION_ADDRESS_3 3 

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS
int received_value=0;



void setup() {

  Serial.begin(9600); // to be able to view the results in the computer's monitor


//ARDUINO  1

  //Tx arduino 1 get start

  if (!rf22.init()) // initialize my radio
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(434.0)) // set the desired frequency
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  ); // set the desired modulation
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1);
 
  delay(1000);

//Rx from arduino 1 when finish

if (!rf22.init())
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(435.0)) // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  );// The modulation should be the same as that of the transmitter. Otherwise no communication will take place
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay 

//ARDUINO 2

 //Tx arduino 2 get start

  if (!rf22.init()) // initialize my radio
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(436.0)) // set the desired frequency
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  ); // set the desired modulation
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_2, DESTINATION_ADDRESS_2);
 
  delay(1000);

//Rx from arduino 2 when finish

if (!rf22.init())
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(437.0)) // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  );// The modulation should be the same as that of the transmitter. Otherwise no communication will take place
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_2, DESTINATION_ADDRESS_2); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay 

//ARDUINO 3

 //Tx arduino 3 get start

  if (!rf22.init()) // initialize my radio
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(438.0)) // set the desired frequency
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  ); // set the desired modulation
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_3, DESTINATION_ADDRESS_3);
 
  delay(1000);

//Rx from arduino 3 when finish

if (!rf22.init())
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(439.0)) // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  );// The modulation should be the same as that of the transmitter. Otherwise no communication will take place
  //modulation

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_3, DESTINATION_ADDRESS_3); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay 








}



  void loop()
{

if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == '1') {
            // Do something when command '1' is received
            
   //sent to arduino 1 get start 
   //Tx code
   char message[] = "Arduino 1 get start";
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
   
        }

  //Rx code receive code from arduino 1
  uint8_t buf[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold incoming data
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
    if (incoming=="finish" && command == '2')
    { 


            //sent to arduino 2 get start 
   //Tx code
   char message[] = "Arduino 2 get start";
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

    }
   
   //Rx code receive code from arduino 2
  uint8_t buf2[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold incoming data
  char incoming2[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold converted incoming data as a string
  memset(buf2, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(incoming2, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  uint8_t len2 = sizeof(buf2); // Length of the incoming data
  uint8_t from2; // Variable to store the sender's address

  // Check if data is received
  if (rf22.recvfromAck(buf2, &len2, &from2)) {
    buf[len] = '\0'; // Ensure null-termination for proper string handling
    memcpy(incoming2, buf2, len2 + 1); // Copy received data into incoming buffer, ensuring it's a valid string

    Serial.print("Message received from address: ");
    Serial.println(from2, DEC); // Display the sender's address
    Serial.print("Message: ");
    Serial.println(incoming2); // Display the received message as a string
    delay(1000);
}

 if (incoming=="finish" && command == '3')
     {


            //sent to arduino 2 get start 
   //Tx code
   char message[] = "Arduino 3 get start";
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

        
        } //end if(command='3')

     //Rx code receive code from arduino 3
  uint8_t buf3[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold incoming data
  char incoming3[RF22_ROUTER_MAX_MESSAGE_LEN]; // Buffer to hold converted incoming data as a string
  memset(buf, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(incoming, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  uint8_t len3 = sizeof(buf); // Length of the incoming data
  uint8_t from3; // Variable to store the sender's address

  // Check if data is received
  if (rf22.recvfromAck(buf3, &len3, &from3)) {
    buf[len3] = '\0'; // Ensure null-termination for proper string handling
    memcpy(incoming3, buf3, len3 + 1); // Copy received data into incoming buffer, ensuring it's a valid string

    Serial.print("Message received from address: ");
    Serial.println(from3, DEC); // Display the sender's address
    Serial.print("Message: ");
    Serial.println(incoming3); // Display the received message as a string
    delay(1000); 

  }

   if (incoming3=="finish" && command == '4')
       Serial.println("end");
    



}
}
