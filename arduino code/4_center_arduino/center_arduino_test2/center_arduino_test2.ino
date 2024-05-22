#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 0 // define my unique address
#define DESTINATION_ADDRESS_1 1 // define who I can talk to
#define DESTINATION_ADDRESS_2 2 // define who I can talk to
#define DESTINATION_ADDRESS_3 3 // define who I can talk to

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS

const char* gates[] = {"OrGate", "AndGate", "NorGate", "NandGate","XorGate"/*,"XnorGate"*/,"NotGate"};
int number_of_bytes=0;

void setup() {
  Serial.begin(9600); // to be able to view the results in the computer's monitor

  if (!rf22.init()) { // initialize my radio
    Serial.println("RF22 init failed");
  }
  
  // Set the desired frequency (common for all communications)
  if (!rf22.setFrequency(442.0)) {
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


       //sendMessage_logical_gates#("Experiment 1 Start");

         sendMessage("Experiment 1 Start",DESTINATION_ADDRESS_1);
      // Select 4 random gates
      int selectedGates[4];
      for (int i = 0; i <4 ; i++) {
        selectedGates[i] = random(0, 6); // Randomly select an index from 0 to 6
      }

      for (int i = 0; i <4; i++) { 

        
       // sendMessage_logical_gates(gates[selectedGates[i]]);
       
        sendMessage(gates[selectedGates[i]],DESTINATION_ADDRESS_1);

        while (true) {
          String receiveGateMessage=receiveMessage();
          if (receiveGateMessage == "Success") {
            Serial.println(receiveGateMessage); // Send direction to Python script
            delay(1000);
          }
          if (receiveGateMessage == "Success Gate"){
             delay(1000);
             break;
           
           
          }
        }
      }

      while(true)
      {
        
        String finish_message=receiveMessage();
       
       
        if(finish_message == "Experiment 1 Finish")
              {   
                
                 Serial.println("Experiment 1 Finish");
                 delay(1000);
                 
                  break;
              }   
      } 

    } else if (command == '2') {

      Serial.println("Experiment 2 Start");
        
        
        sendMessage("Experiment 2 Start", DESTINATION_ADDRESS_2);
            
         //   sendMessage_start_maze("Arduino 2 get start");
            
      while (true) {
      
         String receivedMessage = receiveMessage();

          if (receivedMessage == "Left" || receivedMessage == "Right" || 
            receivedMessage == "Up" || receivedMessage == "Down" || receivedMessage == "No move") {
            Serial.println(receivedMessage); // Send direction to Python script
            
        }
       

        if (........) {  //read from pyton to  finish 
           Serial.println("Experiment 2 Finish");
           sendMessage("Experiment 2 Finish", DESTINATION_ADDRESS_2);
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


