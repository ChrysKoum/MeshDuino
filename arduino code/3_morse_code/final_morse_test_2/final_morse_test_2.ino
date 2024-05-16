
#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

// RFM22 setup
#define MY_ADDRESS 3
#define DESTINATION_ADDRESS_1 0

RF22Router rf22(MY_ADDRESS); // Initiate the RF22 with the sender's address

int tonePin = 2;
int toneFreq = 1000;
int ledPin = 13;
int buttonPin = 8;
int debounceDelay = 90;

int dotLength = 240;
// dotLength = basic unit of speed in milliseconds
// 240 gives 5 words per minute (WPM) speed.
// WPM = 1200/dotLength.
// For other speeds, use dotLength = 1200/(WPM)
//
// Other lengths are computed from dot length
int dotSpace = dotLength;
int dashLength = dotLength * 4;
int letterSpace = dotLength * 3;
int wordSpace = dotLength * 7;
float wpm = 1200. / dotLength;

int t1, t2, onTime, gap;
bool newLetter, newWord, letterFound, keyboardText;
int lineLength = 0;
int maxLineLength = 20;

char *letters[] =
    {
        ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", // A-I
        ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", // J-R
        "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};       // S-Z

char *numbers[] =
    {
        "-----", ".----", "..---", "...--", "....-", // 0-4
        ".....", "-....", "--...", "---..", "----." // 5-9
    };

String dashSeq = "";
char keyLetter, ch;
int i, index;
String decodedLetters = ""; // Holds all decoded letters
int number_of_bytes = 0;    // will be needed to measure bytes of message

float throughput = 0; // will be needed for measuring throughput
int flag_measurement = 0;

int counter = 0;
int initial_time = 0;
int final_time = 0;
bool k = true;

void setup() {
    delay(500);
    pinMode(ledPin, OUTPUT);
    pinMode(tonePin, OUTPUT);
    //pinMode(buttonPin, INPUT_PULLUP);
    
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


    newLetter = false; // if false, do NOT check for end of letter gap
    newWord = false;   // if false, do NOT check for end of word gap
    keyboardText = false;

    Serial.println("Setup complete.");
}



void loop() {
    // Check for received message
    String receivedMessage = receiveMessage();

    if (receivedMessage == "Experiment 3 Start") {
        delay(5000); // Delay for 5 seconds

        // Wait for the word to decode
        while (true) {
            String wordToDecode = receiveMessage();
            if (wordToDecode != "") {
                Serial.print("Word to decode: ");
                Serial.println(wordToDecode); // Display the word to decode
                break;
            }
        }

            sendFinishMessage("Experiment 3 Finish");
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

void flashSequence(char *sequence) {
    int i = 0;
    while (sequence[i] == '.' || sequence[i] == '-') {
        flashDotOrDash(sequence[i]);
        i++;
    }
}

void flashDotOrDash(char dotOrDash) {
    digitalWrite(ledPin, HIGH);
    tone(tonePin, toneFreq);
    if (dotOrDash == '.') {
        delay(dotLength);
    } else {
        delay(dashLength);
    }

    digitalWrite(ledPin, LOW);
    noTone(tonePin);
    delay(dotLength);
}



void sendFinishMessage(const char *message) {
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
    memcpy(data_send, message, strlen(message));
    
    Serial.println("Attempting to send finish message...");

    bool success = false;
    for (int attempt = 0; attempt < 3; attempt++) {  // Retry up to 3 times
        Serial.print("Attempt ");
        Serial.println(attempt + 1);
        if (rf22.sendtoWait(data_send, strlen(message), DESTINATION_ADDRESS_1) == RF22_ROUTER_ERROR_NONE) {
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
