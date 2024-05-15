// morse-decode-encode
// by Oompah
// March 3 2023
// credit to "Programming Arduino" by Simon Monk, (c)2016
// for some of the code lines
//
// Either Key in a Morse code sequence using the button to decode,
// or click in the field in the Serial Monitor, and
// type letters followed by Enter to encode into Morse code.
// The LED and tone will sound while you key in the sequence.
// This sketch decodes sequences with letters or numbers
// and prints them to the serial monitor.
// A beep sounds and "?" prints for unrecognized sequences.
//
// To learn Morse Code, type a word in the Serial Monitor,
// Then try keying in the same word as you heard it.
// Tips: 
//   Keep dots short, and dashes long. 
//   Leave a short space after letters.
//   Leave a longer space after words.
//   Try to make nice clean presses and releases.
//
// Circuit:
// Piezo buzzer or speaker connects to pin 2 and ground
// Button connects between pin 8 and ground
// LED (+) to pin 13, (-) 220 Ohm resistor to ground
//



int received_value=0;
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
  int dashLength = dotLength*4;
  int letterSpace = dotLength*3;
  int wordSpace = dotLength*7; 
  float wpm = 1200./dotLength;
  
int t1, t2, onTime, gap;
bool newLetter, newWord, letterFound, keyboardText;
int lineLength = 0;
int maxLineLength = 20; 

char* letters[] = 
{
".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", // A-I
".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", // J-R 
"...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." // S-Z
};

char* numbers[] = 
{
"-----", ".----", "..---", "...--", "....-", //0-4
".....", "-....", "--...", "---..", "----." //5-9
};

String dashSeq = "";
char keyLetter, ch;
int i, index;
String decodedLetters = "";  // Holds all decoded letters

void setup() 
{
  delay(500);
  pinMode(ledPin, OUTPUT);
  pinMode(tonePin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);

  Serial.println();
  Serial.println("-------------------------------");
  Serial.println("Morse Code decoder/encoder");
  Serial.print("Speed=");
  Serial.print(wpm);
  Serial.print("wpm, ");
  Serial.print("dot=");
  Serial.print(dotLength);
  Serial.println("ms");   
  
// Test the LED and tone
  tone(tonePin, toneFreq);
  digitalWrite(ledPin, HIGH);
  delay(2000);
  digitalWrite(ledPin, LOW);
  noTone(tonePin);
  delay(600);

//flash to demonstrate the expected key speed
//A
   Serial.print("A .-  ");
   index = 'A'-65;
   flashSequence(letters[index]);
   delay(wordSpace);
//B
 //  Serial.print("B -...  ");
 //  index = 'B'-65;
 //  flashSequence(letters[index]);
  // delay(wordSpace);
//C
 //  Serial.print("C -.-.  ");
  // index = 'C'-65;
  // flashSequence(letters[index]);
  // delay(wordSpace);

  Serial.println();
  Serial.println("-------------------------------");
  Serial.println("Click field in Serial Monitor,");
  Serial.println("type text and press Enter, or");
  Serial.println("Key in Morse Code to decode:");
  Serial.println("-------------------------------");
      
  newLetter = false; //if false, do NOT check for end of letter gap
  newWord = false;  //if false, do NOT check for end of word gap
  keyboardText = false; 
}

void loop() 
{

// Check to see if something has been entered on the keyboard

  
if (Serial.available() > 0 )
  {
    if (keyboardText == false) 
    {
      Serial.println();
      Serial.println("-------------------------------");
    }
    keyboardText = true;
    ch = Serial.read();
    if (ch >= 'a' && ch <= 'z')
    { ch = ch-32; }
    
    if (ch >= 'A' && ch <= 'Z')
    {
      Serial.print(ch); 
      Serial.print(" ");
      Serial.println(letters[ch-'A']);
      flashSequence(letters[ch-'A']);
      delay(letterSpace);
    }
    if (ch >= '0' && ch <= '9')
    {
      Serial.print(ch);
      Serial.print(" ");
      Serial.println(numbers[ch-'0']);
      flashSequence(numbers[ch-'0']);
      delay(letterSpace);
    }
    if (ch == ' ')
    {
      Serial.println("_");
      delay(wordSpace);    
    } 

// Print a header after last keyboard text    
     if (Serial.available() <= 0) 
     {
      Serial.println();
      Serial.println("Enter text or Key in:");
      Serial.println("-------------------------------");
      keyboardText = false;
     }
  }
 
  if (digitalRead(buttonPin) == HIGH ) //button is pressed
  {
    newLetter = true; 
    newWord = true;
    t1 = millis(); //time at button press
    digitalWrite(ledPin, HIGH); //turn on LED and tone
    tone(tonePin, toneFreq);
    delay(debounceDelay);     
    while (digitalRead(buttonPin) == HIGH ) // wait for button release
    {
      delay(debounceDelay);
    }
    delay(debounceDelay);
       
    t2 = millis();  //time at button release
    onTime = t2 - t1;  //length of dot or dash keyed in
    digitalWrite(ledPin, LOW); //turn off LED and tone
    noTone(tonePin); 
    
    //check if dot or dash 

    if (onTime <= dotLength * 1.5) //allow for 50% longer 
      {dashSeq += ".";} //build dot/dash sequence
    else 
      {dashSeq += "-";}
  }  //end button press section
  
// look for a gap >= letterSpace to signal end letter
// end of letter when gap >= letterSpace

  gap=millis()-t2; 
  if (newLetter && gap >= letterSpace) {
    letterFound = false;
    keyLetter = '?'; // Default unknown letter

    // Search for matching letter in Morse sequence array
    for (int i = 0; i < 26; i++) {
      if (dashSeq == letters[i]) {
        keyLetter = char(i + 65); // Convert index to ASCII character
        letterFound = true;
        break;
      }
    }

    // Now check numbers if no letter was found
    if (!letterFound) {
      for (int i = 0; i < 10; i++) {
        if (dashSeq == numbers[i]) {
          keyLetter = char(i + 48); // Convert index to ASCII number
          letterFound = true;
          break;
        }
      }
    }
    // Output the found character
    Serial.print(keyLetter);
    decodedLetters += keyLetter; // Append this letter to the sequence

    // Reset for next input
    newLetter = false;
    dashSeq = "";

    // Check if the sequence "ABC" is found
    if (decodedLetters.endsWith("ABC")) {
      
      Serial.println(" Success");  // Output success message
      decodedLetters = ""; // Optionally reset the decoded sequence
    }
  }  
  
// keyed letter has been identified and printed

// when gap is >= wordSpace, insert space between words
// lengthen the word space by 50% to allow for variation

  if (newWord == true && gap>=wordSpace*3)
    { 
     newWord = false; 
     Serial.print("_");  
     lineLength=lineLength+1;
     
// flash to indicate new word

    digitalWrite(ledPin, HIGH);
    delay(25);
    digitalWrite(ledPin, LOW);       
    } 

// insert linebreaks

  if (lineLength >= maxLineLength) 
    {
      Serial.println();
      lineLength = 0;
    }      
} 

void flashSequence(char* sequence)
{
  int i = 0;
  while (sequence[i] == '.' || sequence[i] == '-')
  {
    flashDotOrDash(sequence[i]);
    i++;
  }
}

void flashDotOrDash(char dotOrDash)
{
  digitalWrite(ledPin, HIGH);
  tone(tonePin, toneFreq);
  if (dotOrDash == '.')
   { delay(dotLength); }
     else
   { delay(dashLength); }

  digitalWrite(ledPin, LOW);
  noTone(tonePin);
  delay(dotLength); }


}//end loop
