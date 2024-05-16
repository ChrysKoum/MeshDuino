#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

// RFM22 setup
#define MY_ADDRESS 3
#define DESTINATION_ADDRESS_1 0

RF22Router rf22(MY_ADDRESS); // Initiate the RF22 with the sender's address

void setup() {
    delay(500);
    Serial.begin(9600);
    Serial.println();
    Serial.println("-------------------------------");
    Serial.println("Morse Code decoder/encoder");

    // Rx,Tx code
    if (!rf22.init()) // initialize my radio
        Serial.println("RF22 init failed");
    // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
    if (!rf22.setFrequency(434.0)) // set the desired frequency
        Serial.println("setFrequency Fail");
    rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
    // 1,2,5,8,11,14,17,20 DBM
    rf22.setModemConfig(RF22::OOK_Rb40Bw335); // set the desired modulation

    // Manually define the routes for this network
    rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay
    delay(1000); // delay for 1 s

    Serial.println("Setup complete.");
}

void loop() {
    // Rx code receive code from center Arduino
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

        if (strcmp(incoming, "Experiment 3 Start") == 0) {
            delay(5000); // Delay for 5 seconds

            // Wait for the word to decode
            while (true) {
                if (rf22.recvfromAck(buf, &len, &from)) {
                    buf[len] = '\0';
                    memcpy(incoming, buf, len + 1);
                    Serial.print("Word to decode: ");
                    Serial.println(incoming); // Display the word to decode
                    break;
                }
            }

            delay(5000); // Delay for another 5 seconds
            sendFinishMessage("Experiment 3 Finish");
        }
    }
}

void sendFinishMessage(const char *message) {
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memcpy(data_send, message, strlen(message));

    if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) {
        Serial.println("sendtoWait failed");
    } else {
        Serial.println("sendtoWait Successful");
    }
}
