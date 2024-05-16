#include <RH_RF22.h>
#include <SPI.h>
#include <RF22Router.h>

// RFM22 setup
#define MY_ADDRESS 1
#define DESTINATION_ADDRESS_1 0

RF22Router rf22(MY_ADDRESS);

// constants won't change. They're used here to set pin numbers:
const int button1Pin = 2;     // the number of the pushbutton pin
const int button2Pin = 3;     // the number of the pushbutton pin

const int OutputLedPin =  13;      // the number of the Output LED pin

const int NotGate = 4;
const int OrGate = 5;
const int AndGate = 6;
const int NorGate = 7;
const int NandGate = 8;
const int XorGate = 9;
const int XnorGate = 10;

// variables will change:
int button1State = 0;         // variable for reading the pushbutton status
int button2State = 0;
int GateSelected = 4;          // not gate selected by default
int gateIndex = 1;
// Variables to track the HIGH LOW HIGH LOW sequence
int highSequence[4] = {0, 0, 0, 0};
int highSequenceIndex = 0;

// Variables to track the HIGH HIGH HIGH or LOW LOW LOW sequence
const int SEQUENCE_LENGTH = 10; // Increased length to store more readings
int sequence[SEQUENCE_LENGTH] = {0};
int sequenceIndex = 0;

void setup() {
  Serial.begin(9600);

  // initialize the LED pin as an output:
  pinMode(OutputLedPin, OUTPUT);
  // initialize the pushbutton pins as input:
  for (int i = 4; i <= 10; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);

  // Initialize RF22
  if (!rf22.init()) {
    Serial.println("RF22 init failed");
  }
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(434.0)) { // The frequency should be the same as that of the transmitter. Otherwise no communication will take place
    Serial.println("setFrequency Fail");
  }
  rf22.setTxPower(RF22_TXPOW_20DBM);
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335); // The modulation should be the same as that of the transmitter. Otherwise no communication will take place

  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay
  Serial.println("Set up complete");
}

void loop() {
  // Rx code receive code from center Arduino
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

    if (strcmp(incoming, "Arduino 1 get start") != 0) {
      // It's a gate command, handle it
      handleGateCommand(incoming, gateIndex);
      gateIndex++;
    }
    if (gateIndex == 5) {
      sendMessage("Experiment 1 Finish");
      gateIndex = 1;
    }
  }
}

void handleGateCommand(const char* gate, int gateIndex) {
  Serial.print("Gate command received: ");
  Serial.println(gate);

  // Determine which gate is selected based on the received message
  if (strcmp(gate, "NotGate") == 0) {
    GateSelected = NotGate;
  } else if (strcmp(gate, "OrGate") == 0) {
    GateSelected = OrGate;
  } else if (strcmp(gate, "AndGate") == 0) {
    GateSelected = AndGate;
  } else if (strcmp(gate, "NorGate") == 0) {
    GateSelected = NorGate;
  } else if (strcmp(gate, "NandGate") == 0) {
    GateSelected = NandGate;
  } else if (strcmp(gate, "XorGate") == 0) {
    GateSelected = XorGate;
  } else if (strcmp(gate, "XnorGate") == 0) {
    GateSelected = XnorGate;
  }

  // Perform the selected gate operation
  performGateOperation();

  // Send completion message
  String response = "Gate " + String(gateIndex) + " Completed";
  sendMessage(response.c_str());
}

void performGateOperation() {
  int tempSequence = -1;

  for (int i = 4; i <= 10; i++) {
    digitalWrite(i, LOW);
  }
  digitalWrite(GateSelected, HIGH);

  while (true) {
    // read the state of the pushbutton value every 1 second:
    delay(1000);
    button1State = digitalRead(button1Pin);
    button2State = digitalRead(button2Pin); // Read the state of button2Pin

    // Update the sequence array with the current button1State
    sequence[sequenceIndex] = button1State;
    sequenceIndex = (sequenceIndex + 1) % SEQUENCE_LENGTH;

    // Check if there's any HIGH in the sequence array
    bool foundHigh = false;
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
      if (sequence[i] == HIGH) {
        foundHigh = true;
        break;
      }
    }

    // Set tempSequence based on the foundHigh flag
    if (foundHigh) {
      tempSequence = HIGH;
    } else {
      tempSequence = LOW;
    }

    // Check the gate selected and perform action accordingly:
    if (GateSelected == NotGate) {
      if (tempSequence == HIGH) {
        digitalWrite(OutputLedPin, LOW);
        highSequence[highSequenceIndex] = LOW;
      } else {
        digitalWrite(OutputLedPin, HIGH);
        highSequence[highSequenceIndex] = HIGH;
      }
    } else if (GateSelected == OrGate) {
      if (button1State == HIGH || button2State == HIGH) {
        digitalWrite(OutputLedPin, HIGH);
      } else {
        digitalWrite(OutputLedPin, LOW);
      }
    } else if (GateSelected == AndGate) {
      if (button1State == HIGH && button2State == HIGH) {
        digitalWrite(OutputLedPin, HIGH);
      } else {
        digitalWrite(OutputLedPin, LOW);
      }
    } else if (GateSelected == NorGate) {
      if (button1State == HIGH || button2State == HIGH) {
        digitalWrite(OutputLedPin, LOW);
      } else {
        digitalWrite(OutputLedPin, HIGH);
      }
    } else if (GateSelected == NandGate) {
      if (button1State == HIGH && button2State == HIGH) {
        digitalWrite(OutputLedPin, LOW);
      } else {
        digitalWrite(OutputLedPin, HIGH);
      }
    } else if (GateSelected == XorGate) {
      if (button1State == button2State) {
        digitalWrite(OutputLedPin, LOW);
      } else {
        digitalWrite(OutputLedPin, HIGH);
      }
    } else if (GateSelected == XnorGate) {
      if (button1State == button2State) {
        digitalWrite(OutputLedPin, HIGH);
      } else {
        digitalWrite(OutputLedPin, LOW);
      }
    }
    highSequenceIndex = (highSequenceIndex + 1) % 4;

    // Print the highSequence array
    Serial.print("High Sequence: ");
    for (int i = 0; i < 4; i++) {
      if (highSequence[i] == HIGH) {
        Serial.print("HIGH ");
      } else if (highSequence[i] == LOW) {
        Serial.print("LOW ");
      } else {
        Serial.print("MIXED ");
      }
    }
    Serial.println();

    // Print the sequence array
    Serial.print("Sequence: ");
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
      Serial.print(sequence[i]);
      Serial.print(" ");
    }
    Serial.println();

    // Check for the HIGH LOW HIGH LOW sequence
    if (highSequence[0] == HIGH && highSequence[1] == LOW && highSequence[2] == HIGH && highSequence[3] == LOW) {
      Serial.println("Condition success");
      sendMessage("Finish");
      break;
    }
  } // while
}

void sendMessage(const char* message) {
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memcpy(data_send, message, strlen(message));

  if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) {
    Serial.println("sendtoWait failed");
  } else {
    Serial.println("sendtoWait Successful");
  }
}
