#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 0 // define my unique address
#define DESTINATION_ADDRESS_1 1 // define who I can talk to

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
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      Serial.println("Experiment 1 Start");

      // Send gate commands and wait for responses
      for (int i = 0; i < 4; i++) {
        // Wait for gate command from Serial (from Python script)
        while (!Serial.available()) { delay(10); }
        String gate = Serial.readStringUntil('\n');
        gate.trim();

        // Send the gate command to the first Arduino
        sendMessage(gate.c_str(), DESTINATION_ADDRESS_1);

        // Wait for the corresponding "Gate Completed" response
        String expectedResponse = "Gate " + String(i+1) + " Completed";
        while (true) {
          String receivedMessage = receiveMessage();
          if (receivedMessage == expectedResponse) {
            Serial.println(receivedMessage); // Print so Python can read it
            break;
          }
        }
      }

      // Finally, wait for the "Experiment 1 Finish" message
      while (true) {
        String receivedMessage = receiveMessage();
        if (receivedMessage == "Experiment 1 Finish") {
          Serial.println("Experiment 1 Finish");
          break;
        }
      }
    } else if (command == '2') {
      Serial.println("Experiment 2 Start");
      while (true) {
        sendMessage("Arduino 2 get start", DESTINATION_ADDRESS_1);
        String receivedMessage = receiveMessage();
        if (receivedMessage == "Experiment 2 Finish") {
          Serial.println("Experiment 2 Finish");
          break;
        }
      }
    } else if (command == '3') {
      Serial.println("Experiment 3 Start");
      while (true) {
        sendMessage("Arduino 3 get start", DESTINATION_ADDRESS_3);
        String receivedMessage = receiveMessage();
        if (receivedMessage == "Experiment 3 Finish") {
          Serial.println("Experiment 3 Finish");
          break;
        }
      }
    }
  }
}

void sendMessage(const char* message, uint8_t destination) {
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memcpy(data_send, message, strlen(message));
  
  if (rf22.sendtoWait(data_send, strlen(message), destination) != RF22_ROUTER_ERROR_NONE) {
    Serial.println("sendtoWait failed");
  } else {
    Serial.println("sendtoWait Successful");
  }
  delay(1000);
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
    delay(1000);
    
    return String(incoming);
  }
  return "";
}
