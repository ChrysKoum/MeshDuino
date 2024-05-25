#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 0 // define my unique address
#define DESTINATION_ADDRESS_1 1 // define who I can talk to
#define DESTINATION_ADDRESS_2 2 // define who I can talk to
#define DESTINATION_ADDRESS_3 3 // define who I can talk to

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS

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

       
      Serial.println("Experiment 1 Start");

      sendMessage("e1s",DESTINATION_ADDRESS_1);
      // Wait for the word that needs decoding
      for (int i = 0; i <1; i++) { 
        while (true) {
          if (Serial.available()) {
            String gate = Serial.readStringUntil('\n');
            gate.trim();
            Serial.println("gate: " + String(gate));

            if (gate == "NotGate") {
                Serial.println("NotGate"); // Print full name
                sendMessage("n", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "OrGate") {
                Serial.println("OrGate"); // Print full name
                sendMessage("o", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "AndGate") {
                Serial.println("AndGate"); // Print full name
                sendMessage("a", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "NorGate") {
                Serial.println("NorGate"); // Print full name
                sendMessage("no", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "NandGate") {
                Serial.println("NandGate"); // Print full name
                sendMessage("na", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "XorGate") {
                Serial.println("XorGate"); // Print full name
                sendMessage("xo", DESTINATION_ADDRESS_1); // Send shorthand version
            } else if (gate == "XnorGate") {
                Serial.println("XnorGate"); // Print full name
                sendMessage("xn", DESTINATION_ADDRESS_1); // Send shorthand version
            }

            break;
          }
        }


        while (true) {
          String receiveGateMessage=receiveMessage();
          if (receiveGateMessage == "s") {
            Serial.println(receiveGateMessage); // Send direction to Python script
            delay(1000);
          }
          if (receiveGateMessage == "sg"){
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
        
        
        sendMessage("e2s", DESTINATION_ADDRESS_2);
            
         //   sendMessage_start_maze("Arduino 2 get start");
            
      while (true) {

         String receivedMessage = receiveMessage();

          if (receivedMessage == "l" || receivedMessage == "r" || 
            receivedMessage == "u" || receivedMessage == "d" || receivedMessage == "n") {

            if (receivedMessage == "l") {
                Serial.println("Left"); // Send direction to Python script
            } else if (receivedMessage == "r") {
                Serial.println("Right"); // Send direction to Python script
            } else if (receivedMessage == "u") {
                Serial.println("Up"); // Send direction to Python script
            } else if (receivedMessage == "d") {
                Serial.println("Down"); // Send direction to Python script
            } else if (receivedMessage == "n") {
                Serial.println("No move"); // Send direction to Python script
            }
        }

      
      }
       
      if (Serial.available()) {
        Serial.println("Experiment 2 Finish");
        String message = Serial.readStringUntil('\n');
        message.trim();
        if(message == "Experiment 2 Finish"){
          sendMessage("e2f", DESTINATION_ADDRESS_2);
        }
        break; 
      }

    }


    } else if (command == '3') {
      Serial.println("Experiment 3 Start");
      sendMessage("e3s", DESTINATION_ADDRESS_3);

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
        if (receivedMessage == "e3f") {
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
        Serial.println("Failed to send finish message after 5 attempts.");
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


