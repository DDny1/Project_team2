void setup() {
    Serial.begin(9600);
}

void loop() {
  char rx_val = 'z';
  unsigned int asd = 10;

  if (Serial.available()) {
    rx_val = Serial.read();

    if (rx_val == 'a') { //손 핌 후진
      asd = 0;
    } else if(rx_val == 'b') { //조향각 3 75도
      asd = 1;
    } else if(rx_val == 'c') { //조향각 2 60도
      asd = 2;
    } else if(rx_val == 'd') { //조향각 1 45도
      asd = 3;
    } else if(rx_val == 'e') { //조향각 5 105도
      asd = 4;
    } else if(rx_val == 'f') { //조향각 6 120도
      asd = 5;
    } else if(rx_val == 'g') { //조향각 7 135도
      asd = 6;
    } else if(rx_val == 'h') { //정지
      asd = 7;
    } else if(rx_val == 'i') { //전진
      asd = 8;
    } else if(rx_val == 'j') { //90도
      asd = 9;
    } else {
      asd = 10;
    }
  }

  if (asd != 10) {
    Serial.println(asd);
    delay(1000);
  }

}
