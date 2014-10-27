unsigned long serialdata;
int inbyte;
int attachedServos[80] = {};
int pinNumber;
int sensorVal;
int analogRate;
int digitalState;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  getSerial();
  switch(serialdata)
  {
  case 1:
    {
      //analog digital write
      getSerial();
      switch (serialdata)
      {
      case 1:
        {
          //analog write
          getSerial();
          pinNumber = serialdata;
          getSerial();
          analogRate = serialdata;
          pinMode(pinNumber, OUTPUT);
          analogWrite(pinNumber, analogRate);
          pinNumber = 0;
          break;
        }
      case 2:
        {
          //digital write
          getSerial();
          pinNumber = serialdata;
          getSerial();
          digitalState = serialdata;
          pinMode(pinNumber, OUTPUT);
          if (digitalState == 1)
          {
            digitalWrite(pinNumber, LOW);
          }
          if (digitalState == 2)
          {
            digitalWrite(pinNumber, HIGH);
          }
          pinNumber = 0;
          break;
         
        }
     }
     break; 
    }
    case 2:
    {
      getSerial();
      switch (serialdata)
      {
      case 1:
        {
          //analog read
          getSerial();
          pinNumber = serialdata;
          pinMode(pinNumber, INPUT);
          sensorVal = analogRead(pinNumber);
          Serial.println(sensorVal);
          sensorVal = 0;
          pinNumber = 0;
          break;
        } 
      case 2:
        {
          //digital read
          getSerial();
          pinNumber = serialdata;
          pinMode(pinNumber, INPUT);
          sensorVal = digitalRead(pinNumber);
          Serial.println(sensorVal);
          sensorVal = 0;
          pinNumber = 0;
          break;
        }
      }
      break;
    }
    case 3:
    {
      getSerial();
      switch(serialdata)
      {
        case 1:
        {
        }
        case 2:
        {
        }
        case 3:
        {
          softReset();
        }
      }
      break;
    }
  }
}

long getSerial()
{
  serialdata = 0;
  while (inbyte != '/')
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != '/')
    {
     
      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}

void softReset(){
  asm volatile ("  jmp 0");
}