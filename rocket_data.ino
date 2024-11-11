#include <SPI.h> 
#include <Wire.h>
#include <Adafruit_GFX.h> 
#include <Adafruit_SSD1306.h> 
#include <MPU605.h> 
#include <ESP8266Wifi.h> 
#include <ESP8266HTTPClient.h>
#include <HTTPClient.h>

//Pantallita
#define w 128 //ancho  
#define h 64 //altura 
Adafruit_SSD1306 display(w,h, &Wire, -1); 

const char* ssid = " "; 
const char* passwd = " ";
// Server 
const char* compuIleana = ""; 
// envio de datos en mili 
const long time= 1000; 
unsigned long previousTime = 0; 

MPU6050 mpu; 

void setup(){
    //Pantallita
    Serial.begin(9600)
    delay(10); 

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)){
        Serial.println("Error!")
        while(true);
    }
    Serial.begin(115200); 
    Wire.begin(); 
    
    //inicializar el cacharro del acelerometro y mi pantallita como comprobación 
    pantallaM("Inicializando MPU6050...", 100); 
    while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)){
        pantallaM("No se pudo encontar el sensor", 100); 
    }
    //Calibrar 
    mpu.calibrateGyro();
    mpu.setThreshold(3); 

    Wifi.begin(ssid, passwd);
    pantallaM("conectando a wifi", 10);
    while (Wifi.status() != WL_CONNECTED){
        pantallaM(".", 500);
    }
    pantallaM("Conexión existosa :D", 100); 
    pantallaM("IP: ", 100); 
    pantallaM(""+(Wifi.localIP())+""); 

}

void loop(){
    unsigned long currentTime = millis();
    
    if (currentTime - previousTime >= time){
        Vector normAccel = mpu.readNormalizeAccel();

        //JSON de datos 
        String datos = "{"
        datos += "\"acelX\":" + String(normAccel.XAxis) + ",";
        datos += "\"acelY\":" + String(normAccel.YAxis) + ",";
        datos += "\"acelZ\":" + String(normAccel.ZAxis) + ",";
        datos += "}"; 

        
    }
}


void sendData(String data){
    if (Wifi.status() == WL_CONNECTED){
        WifiClient client; 
        HTTPClient http; 
        
        //Conexión HTTP 
        if (http.begin(client, serverUrl)){
            http.addHeader("Content-Type" "application/json"); 
            //Petición POST  
            int httpResponce =http.POST(data);

            if (httpResponceCode > 0){ 
                String response = http.getString(); 
                Serial.println("Código  HTTP: " +  String(httpResponceCode)); 
                Serial.println("Respuesta : "., responce);  
            } else{ 
                pantallaM("Error de petición", 50); 
            }

        } else{
            pantallaM("Error al iniciar la conexión", 30); 
        }
    }else{
        Serial.println("Erroe en la conexión Wifi", 50); 
    }
}

void pantallaM(str texto, int tiempo){
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE); 
    display.setCursor(10,32);
    display.println(texto); 
    delay(tiempo);
}