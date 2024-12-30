#include "DHT.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#define LED 2

const char* ssid = "SFR_C08F";
const char* password = "idi93i5pn6hy256hxdw8";
const char* serverUrl = "http://192.168.1.210:8000/ADDMesuresJson/";
// Broche DHT
#define DHTPIN 12 //GPIO12 D6
// Definit le type de capteur utilise
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(9600);
  
  // Conection WIFI
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 

  // Initialise la capteur DHT22
  dht.begin();

}
void loop() {

  // Recupere la temperature et l'humidite du capteur et l'affiche
  // sur le moniteur serie
  String TemperatureValue = String(dht.readTemperature());
  String HumidityValue = String(dht.readHumidity());

  Serial.println("Temperature = " + TemperatureValue +" °C");
  Serial.println("Humidite = " + HumidityValue +" %");
  


 // HTTP POST
   if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    WiFiClient client;
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    int valeur = dht.readHumidity();         
    int id_capteur = 1;      
    String jsonPayload = "{\"valeur\":" + String(valeur) + ",\"id_capteur\":" + String(id_capteur) + "}";
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.println("POST successful");
      String response = http.getString();
      Serial.println("Server Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    valeur = dht.readTemperature();         
    id_capteur = 2;      
    jsonPayload = "{\"valeur\":" + String(valeur) + ",\"id_capteur\":" + String(id_capteur) + "}";
    httpResponseCode = http.POST(jsonPayload);      



    if (httpResponseCode > 0) {
      Serial.println("POST successful");
      String response = http.getString();
      Serial.println("Server Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi disconnected");
  }
  // Attend 10 min avant de reboucler
  delay(600000);
}