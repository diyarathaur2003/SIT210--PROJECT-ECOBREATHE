#include <DFRobot_ENS160.h>
#include "Firebase_Arduino_WiFiNINA.h"
#include <Wire.h>
#include "PMS.h"
#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
// #include <Arduino.h>

DFRobot_ENS160_I2C ENS160(&Wire, 0x53);  // Change the I2C address if needed
PMS pms(Serial1);
PMS::DATA data;

const int soil_moisture = A2;
const int indicator = 9;
const int relay = 2;

#define DATABASE_URL "sensor-data-910f3-default-rtdb.firebaseio.com"
#define DATABASE_SECRET "AIzaSyAWUUWU3mlrSh7rl_98PUNGbrexEoxOfWY"

#define WIFI_SSID "diya"
#define WIFI_PASSWORD "1234567890"

WiFiClient client;

// IFTTT Webhook settings
char   HOST_NAME[] = "maker.ifttt.com";
String PATH1   = "/trigger/water_level/with/key/nP4nICF9HRfNhd2dH8gXsnjC0sweR8kA7oRy5V1uJfQ";
String queryString = "?value1=57&value2=25";

FirebaseData fbdo;

bool waterLevelLowFlag = false;

void setup(void) {
  Serial.begin(9600);
  Serial1.begin(9600);
  
  pinMode(soil_moisture, INPUT);
  pinMode(relay, OUTPUT);
  pinMode(indicator, INPUT);
  // digitalWrite(relay, LOW);

  while (NO_ERR != ENS160.begin()) {
    Serial.println("Communication with device failed, please check connection");
    delay(3000);
  }
  Serial.println("Begin ok!");
  ENS160.setPWRMode(ENS160_STANDARD_MODE);
  ENS160.setTempAndHum(25.0, 50.0);

  // Connect to Wi-Fi and Firebase
  Serial.print("Connecting to Wi-Fi");
  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print(".");
    delay(100);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  Firebase.begin(DATABASE_URL, DATABASE_SECRET, WIFI_SSID, WIFI_PASSWORD);
  Firebase.reconnectWiFi(true);
}

void water_ifttt()
{
  if (client.connect(HOST_NAME, 80)) {
    Serial.println("Connected to server");
  }
  else {
    Serial.println("Connection Failed");
  }

  client.println("GET " + PATH1 + queryString + " HTTP/1.1");
  client.println("Host: " + String(HOST_NAME));
  client.println("Connection: close");
  client.println();

  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      Serial.print(c);
    }
  }

  client.stop();
  Serial.println();
  Serial.println("disconnected");
}

void loop() {
  if (pms.read(data)) {

    Serial.print("PM 1.0 (ug/m3): ");
    Serial.println(data.PM_AE_UG_1_0);
    Serial.print("PM 2.5 (ug/m3): ");
    Serial.println(data.PM_AE_UG_2_5);

    Serial.print("PM 10.0 (ug/m3): ");
    Serial.println(data.PM_AE_UG_10_0);

    uint8_t Status = ENS160.getENS160Status();
    Serial.print("Sensor operating status : ");
    Serial.println(Status);

    uint8_t AQI = ENS160.getAQI();
    Serial.print("Air quality index : ");
    Serial.println(AQI);

    uint16_t TVOC = ENS160.getTVOC();
    Serial.print("Concentration of total volatile organic compounds : ");
    Serial.print(TVOC);
    Serial.println(" ppb");

    uint16_t ECO2 = ENS160.getECO2();
    Serial.print("Carbon dioxide equivalent concentration : ");
    Serial.print(ECO2);
    Serial.println(" ppm");

    int moist = analogRead(soil_moisture);
    int level = digitalRead(indicator);  // Use digitalRead for digital inputs

    if (level == LOW && !waterLevelLowFlag) {
      water_ifttt();
      waterLevelLowFlag = true;  // Set the flag to true to prevent repeated triggers
    } else if (level == HIGH) {
      waterLevelLowFlag = false;  // Reset the flag when water level goes back to high
    }
    Serial.println(level);
    Serial.println(moist);
    Firebase.getString(fbdo, "/sensing/mode");
    String mode = fbdo.stringData();  // Store mode in a variable for reuse
    Firebase.getString(fbdo, "/sensing/pump");
    String pump = fbdo.stringData();  // Store pump in a variable for reuse

    if (mode == "Automatic") {
      if (moist > 450 && level == HIGH) {
        digitalWrite(relay, HIGH);
      }

      if (moist < 450 || level == LOW) {
        digitalWrite(relay, LOW);
      }
      if (moist < 450 && level == LOW) {
        digitalWrite(relay, LOW);
      }
    }

    if (mode == "Manual") {
      if (pump == "on") {
        digitalWrite(relay, HIGH);
      } else if (pump == "off") {
        digitalWrite(relay, LOW);
      }
    }


    // Send data to Firebase
    String path = "/sensor_data";  // Change this path to your desired Firebase path
    String jsonStr = "{\"AQI\":" + String(AQI) + ",\"TVOC\":" + String(TVOC) + ",\"ECO2\":" + String(ECO2) + ",\"PMS1_0\":" + String(data.PM_AE_UG_1_0) + ",\"PMS2_5\":" + String(data.PM_AE_UG_2_5) + ",\"PMS10\":" + String(data.PM_AE_UG_10_0) + ",\"soil_moist\":" + String(moist) + ",\"water_level\":" + String(level) + "}";

    if (Firebase.setJSON(fbdo, path, jsonStr)) {
      Serial.println("Data sent to Firebase");
    } else {
      Serial.println("Error sending data to Firebase");
      Serial.println("Error reason: " + fbdo.errorReason());
    }

    Serial.println();
    delay(1000);  // Adjust the delay as needed
  }
}