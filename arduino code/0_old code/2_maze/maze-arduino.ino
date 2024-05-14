const int FORCE_SENSOR_PIN=A1;
const int PHOTO_RESISTOR_PIN=A0;
const int TRIG_PIN_RIGHT=13;
const int ECHO_PIN_RIGHT=12;
const int TRIG_PIN_LEFT=11;
const int ECHO_PIN_LEFT=10;

#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

float duration_right,duration_left,distance_right,distance_left;

 int forceValue=0;
int lightValue=0;

void setup() {
  

  
  pinMode(TRIG_PIN_RIGHT, OUTPUT);
  pinMode(ECHO_PIN_RIGHT, INPUT);
  
  pinMode(TRIG_PIN_LEFT, OUTPUT);
  pinMode(ECHO_PIN_LEFT, INPUT);
  
  pinMode(FORCE_SENSOR_PIN, INPUT); // Configure force sensor pin as input
  
  pinMode(PHOTO_RESISTOR_PIN, INPUT); // Configure photoresistor pin as input
  
    Serial.begin(9600);
}



void loop() {
 
 //for the right 
  digitalWrite(TRIG_PIN_RIGHT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN_RIGHT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN_RIGHT, LOW);
  
  duration_right = pulseIn(ECHO_PIN_RIGHT, HIGH);
  distance_right = (duration_right*.0343)/2;
 // Serial.print("Distance: ");
  //Serial.println(distance);
  //delay(100);
  
  
  //for the left
  digitalWrite(TRIG_PIN_LEFT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN_LEFT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN_LEFT, LOW);
  
  duration_left = pulseIn(ECHO_PIN_LEFT, HIGH);
  distance_left = (duration_left*.0343)/2;
  //Serial.print("Distance: ");
  //Serial.println(distance);
 // delay(100);

  forceValue = analogRead(FORCE_SENSOR_PIN);
  lightValue = analogRead(PHOTO_RESISTOR_PIN);
bool k=false;
 if ( distance_right < 100) {
  // Move right
  Serial.println("Moving Right");
  // Add your code to move right here
   k=true;
  delay(1000);

}

if(distance_left < 100) {
  // Move left
  Serial.println("Moving Left");
  // Add your code to move left here
  k=true;
  delay(1000);
 
}

if (forceValue > 300) {
  // Move down
  Serial.println("Moving Down");
  Serial.println(forceValue);
  // Add your code to move down here
  k=true;
  delay(1000);
  
}

if (lightValue > 500) {
  // Move up
  Serial.println("Moving Up");
  Serial.println(lightValue);
  // Add your code to move up here
  k=true;
  
  delay(1000);
  
}

if (k==false) {
  // If none of the conditions are met
  Serial.println("Nothing");
  // Add your code for no movement here
  delay(1000);
}
  

  
}
