#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 0 // define my unique address
#define DESTINATION_ADDRESS_1 1 // define who I can talk to
#define DESTINATION_ADDRESS_2 2 // define who I can talk to
#define DESTINATION_ADDRESS_3 3 // define who I can talk to

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS

void setup() {
  Serial.begin(9600); // to be able to view the results in the computer's monitor

  if (!rf22.init()) { // initialize my radio
    Serial.println("RF22 init failed");
  }
  
  // Set the desired frequency (common for all communications)
  if (!rf22.setFrequency(434.0)) {
    Serial.println("setFrequency Fail");
  }
  
  // Set the desired power and modulation
  rf22.setTxPower(RF22_TXPOW_20DBM);
  rf22.setModemConfig(RF22::OOK_Rb40Bw335);
  
  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1);
  rf22.addRouteTo(DESTINATION_ADDRESS_2, DESTINATION_ADDRESS_2);
  rf22.addRouteTo(DESTINATION_ADDRESS_3, DESTINATION_ADDRESS_3);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {


       sendMessage_logical_gates("Experiment 1 Start");

      // Select 4 random gates
      int selectedGates[4];
      for (int i = 0; i <4 ; i++) {
        selectedGates[i] = random(0, 6); // Randomly select an index from 0 to 6
      }

      for (int i = 0; i <4; i++) { 
        sendMessage_logical_gates(gates[selectedGates[i]]);
        while (true) {
            
          if (receiveMessage() =="Success"){
             delay(1000);
             break;
           
           
          }
        }
      }

      while(true)
      {
        
        String finish_message=receiveMessage();
           delay(1000);

        if(finish_message == "finish")
              {
                 Serial.println("finish 1");
                  break;
              }   
                      
        
         


      } 

    } else if (command == '2') {

      Serial.println("Experiment 2 Start");
        // sendMessage("Arduino 2 get start", DESTINATION_ADDRESS_2);
            
            sendMessage_start_maze("Arduino 2 get start");
            
      while (true) {
      
         String receivedMessage = receiveMessage();

          if (receivedMessage == "left" || receivedMessage == "right" || 
            receivedMessage == "up" || receivedMessage == "down" || receivedMessage == "no move") {
            Serial.println(receivedMessage); // Send direction to Python script
            delay(1000);
            
        }
        // start with while If the message is left,right,up down, then send it to the python with Serial.println
        if (receivedMessage == "Experiment 2 Finish") {
          Serial.println("Experiment 2 Finish");
          break;
        }
      }
    } else if (command == '3') {
      Serial.println("Experiment 3 Start");
      sendMessage("Experiment 3 Start", DESTINATION_ADDRESS_3);

      // Wait for the word that needs decoding
      while (true) {
        if (Serial.available()) {
          String wordToDecode = Serial.readStringUntil('\n');
          wordToDecode.trim();
          Serial.println("wordToDecode: " + String(wordToDecode));
          sendMessage(wordToDecode.c_str(), DESTINATION_ADDRESS_3);
          break;
        }
      }

      // Wait for the "Experiment 3 Finish" message
      while (true) {
        String receivedMessage = receiveMessage();
        if (receivedMessage == "Experiment 3 Finish") {
          Serial.println("Experiment 3 Finish");
          break;
        }
      }
    }
  }
}

void sendMessage_start_maze(const char* message) {
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memcpy(data_send, message, strlen(message));

  if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_2) != RF22_ROUTER_ERROR_NONE) { //put destination 2
    Serial.println("sendtoWait failed");
  } else {
    Serial.println("sendtoWait Successful");
  }
}

void sendMessage_logical_gates(const char* message) {
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memcpy(data_send, message, strlen(message));

  if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) { //put destination1 
    Serial.println("sendtoWait failed"); 
  } else {
    Serial.println("sendtoWait Successful");
  }
}

void sendMessage(const char *message, uint8_t destination) {
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memcpy(data_send, message, strlen(message));
    
    Serial.println("Attempting to send finish message...");

    bool success = false;
    for (int attempt = 0; attempt < 5; attempt++) {  // Retry up to 3 times
        Serial.print("Attempt ");
        Serial.println(attempt + 1);
        if (rf22.sendtoWait(data_send, strlen(message), destination) == RF22_ROUTER_ERROR_NONE) {
            Serial.println("sendtoWait Successful");
            success = true;
            break;
        } else {
            Serial.println("sendtoWait failed");
        }
        delay(1000); // Wait 1 second before retrying
    }

    if (!success) {
        Serial.println("Failed to send finish message after 3 attempts.");
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


