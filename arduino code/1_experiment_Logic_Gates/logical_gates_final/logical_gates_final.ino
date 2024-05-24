#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 1 // define my unique address
#define DESTINATION_ADDRESS_1 0 // define who I can talk to

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS

// constants won't change. They're used here to set pin numbers:
const int button1Pin = 15; // the number of the pushbutton pin
const int button2Pin = 16; // the number of the pushbutton pin
const int OutputLedPin = 13; // the number of the Output LED pin
const int NotGate = 3;
const int OrGate = 4;
const int AndGate = 5;
const int NorGate = 6;
const int NandGate = 7;
const int XorGate = 8;
const int XnorGate =9; 
int number_of_bytes=0;
// variables will change:
int button1State = 0; // variable for reading the pushbutton status
int button2State = 0;
int cnt = 0; // counter for condition checks

void sendMessage(const char* message);
String receiveMessage();

// Define conditions for each gate
bool orConditions[4][3] = {
    {LOW, LOW, LOW}, 
    {LOW, HIGH, HIGH}, 
    {HIGH, LOW, HIGH}, 
    {HIGH, HIGH, HIGH}
};

bool andConditions[4][3] = {
    {LOW, LOW, LOW}, 
    {LOW, HIGH, LOW}, 
    {HIGH, LOW, LOW}, 
    {HIGH, HIGH, HIGH}
};

bool norConditions[4][3] = {
    {LOW, LOW, HIGH}, 
    {LOW, HIGH, LOW}, 
    {HIGH, LOW, LOW}, 
    {HIGH, HIGH, LOW}
};

bool nandConditions[4][3] = {
    {LOW, LOW, HIGH}, 
    {LOW, HIGH, HIGH}, 
    {HIGH, LOW, HIGH}, 
    {HIGH, HIGH, LOW}
};

bool xorConditions[4][3] = {
    {LOW, LOW, LOW}, 
    {LOW, HIGH, HIGH}, 
    {HIGH, LOW, HIGH}, 
    {HIGH, HIGH, LOW}
};

bool xnorConditions[4][3] = {
    {HIGH, LOW, LOW}, 
    {LOW, HIGH, LOW}, 
    {LOW, LOW, HIGH}, 
    {HIGH, HIGH, HIGH}
};

bool notConditions[2][2] = {
    {LOW, HIGH}, 
    {HIGH, LOW}
};

int cnt2 = 0;

void setup() {
  pinMode(OutputLedPin, OUTPUT);
  for (int i = 4; i <= 10; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);

  Serial.begin(9600);
 
  if (!rf22.init()) {
    Serial.println("RF22 init failed");
  }

  if (!rf22.setFrequency(432.0)) {
    Serial.println("setFrequency Fail");
  }

  rf22.setTxPower(RF22_TXPOW_20DBM);
  rf22.setModemConfig(RF22::OOK_Rb40Bw335);

  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1);
  delay(1000);
  Serial.println("setup complete");
}

void loop() {
  String start_message = receiveMessage();

  if (start_message == "e1s") {
    while (true) {
      String receivedMessage = receiveMessage();

      // Reset all gate LEDs to LOW
      for (int i = 4; i <= 10; i++) {
        digitalWrite(i, LOW);
      }

      if (receivedMessage == "o") { // Or Gate
        digitalWrite(OrGate, HIGH);
        checkConditions(orConditions, 4);
      } else if (receivedMessage == "a") { // And Gate
        digitalWrite(AndGate, HIGH);
        checkConditions(andConditions, 4);
      } else if (receivedMessage == "no") { // Nor Gate
        digitalWrite(NorGate, HIGH);
        checkConditions(norConditions, 4);
      } else if (receivedMessage == "na") { // Nand Gate
        digitalWrite(NandGate, HIGH);
        checkConditions(nandConditions, 4);
      } else if (receivedMessage == "xo") { // Xor Gate
        digitalWrite(XorGate, HIGH);
        checkConditions(xorConditions, 4);
      } else if (receivedMessage == "xn") { // Xnor Gate
        digitalWrite(XnorGate, HIGH);
        checkConditions(xnorConditions, 4);
      } else if (receivedMessage == "n") { // Not Gate
        digitalWrite(NotGate, HIGH);
        checkNotConditions(notConditions, 2);
      }

      if (cnt2 == 1) {
        Serial.println("Finished");
        delay(1000);
        sendMessage("f");
        delay(2000);
        while (true) {
          Serial.println("ended");
          delay(100000);
        }
      }
    }
  }
}

void checkConditions(bool conditions[][3], int size) {
  cnt = 0;
  cnt2++;

  for (int i = 0; i < size; i++) {
    Serial.println("YOU HAVE TO DO THE FOLLOW COMBINATION:");
    Serial.print("Button1: ");
    Serial.print(conditions[i][0]);
    Serial.print(" Button2: ");
    Serial.print(conditions[i][1]);
    Serial.print(" LED: ");
    Serial.println(conditions[i][2]);
    Serial.print(" cnt: ");
    Serial.println(cnt);

    while (i == cnt) {
      digitalWrite(OutputLedPin, LOW);
      button1State = digitalRead(button1Pin);
      button2State = digitalRead(button2Pin);

      // Add a small delay for debouncing
      delay(50);

      if (button1State == conditions[i][0] && button2State == conditions[i][1]) {
        cnt++;
        digitalWrite(OutputLedPin, conditions[i][2]);
        delay(1000);
        Serial.println("Success");
        sendMessage("s");

         break;
        
      }
    }

  }
    delay(1000);
    sendMessage("sg");
    delay(1000);

  }


void checkNotConditions(bool conditions[][2], int size) {
  cnt = 0;
  cnt2++;

  for (int i = 0; i < size; i++) {
    Serial.println("YOU HAVE TO DO THE FOLLOW COMBINATION:");
    Serial.print("Button1: ");
    Serial.print(conditions[i][0]);
    Serial.print(" LED: ");
    Serial.println(conditions[i][1]);
    Serial.print(" cnt: ");
    Serial.println(cnt);

    while (i == cnt) {
      digitalWrite(OutputLedPin, HIGH);
      button1State = digitalRead(button1Pin);

      if (button1State == conditions[i][0]) {
        digitalWrite(OutputLedPin, conditions[i][1]);
        delay(1000);
        Serial.println("Success");
        sendMessage("s");
        cnt++;
      }
    }
  }

  delay(1000);
  sendMessage("sg");
  delay(1000);
}

void sendMessage(const char *message) {
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memcpy(data_send, message, strlen(message));

    Serial.println("Attempting to send message...");

    bool success = false;
    for (int attempt = 0; attempt < 5; attempt++) {  // Retry up to 5 times
        Serial.print("Attempt ");
        Serial.print(attempt + 1);
        Serial.print(": Sending message to destination ");
        Serial.println(DESTINATION_ADDRESS_1);

        if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) == RF22_ROUTER_ERROR_NONE) {
            Serial.println("sendtoWait Successful");
            success = true;
            number_of_bytes+=sizeof(data_send); // I'm counting the number of bytes of my message
            Serial.print("Number of Bytes= ");
            Serial.println(number_of_bytes);//
            break;
        } else {
            Serial.println("sendtoWait failed");
        }
        delay(2000); // Wait 2 seconds before retrying
            Serial.println("retring");
    }

    if (!success) {
        Serial.println("Failed to send message after 5 attempts.");
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
