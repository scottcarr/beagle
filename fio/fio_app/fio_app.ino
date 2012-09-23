#include <Wire.h>

#define PACKET_SIZE     (5)
#define CMD_ID_WRITE    (0x01)
#define CMD_ID_READ     (0x02)

char readFromI2C(char chip_addr, char reg_addr, char num, char* buff) 
{
    Wire.beginTransmission(chip_addr);
    Wire.write(reg_addr);
    Wire.endTransmission();
    Wire.beginTransmission(chip_addr);
    Wire.requestFrom(chip_addr, num); 
    int i;
    for (i = 0; i < num; i++) {
        while(!Wire.available()); // wait for recv
        buff[i++] = Wire.read();
    }
    Wire.endTransmission();
}

void setup()
{
    Serial.begin(57600);
    Wire.begin();

}

char isPacketAvailable()
{
    if (Serial.available() == PACKET_SIZE) {
        return 1;
    } else {
        return 0;
    }
}

char isValidPacket(char cmd_id, char chip_addr, char reg_addr, char num_read)
{
    // validate cmd_id
    if ( (cmd_id == CMD_ID_READ) ||  (cmd_id == CMD_ID_READ) )  {
        // good cmd_id
    } else {
        // bad cmd_id
        return 0;
    }

    // validate chip addr
    if ( (chip_addr <= 0x7F) && (chip_addr >= 0x00) ) {
        // good chip_addr
    } else {
        // bad chip_addr
        return 0;
    }

    // validate register addr
    if ( (reg_addr <= 0x7F) && (reg_addr >= 0x00) ) {
        // good reg_addr
    } else {
        // bad reg_addr
        return 0;
    }

    // validate num_read
    if ( (num_read > 0x00) && (num_read + reg_addr <= 0x7F)) {
        // good num_read
    } else {
        // bad num_read
        return 0;
    }
    
    // if we get here, all the checks are OK
    return 1;
}

void respondToPacket()
{
    char buff[PACKET_SIZE];
    Serial.readBytes(buff, PACKET_SIZE);
    char cmd_id = buff[0];
    char chip_addr = buff[1];
    char reg_addr = buff[2];
    char num_read = buff[3];
    switch(cmd_id) {
        case CMD_ID_READ:
            if(isValidPacket(cmd_id, chip_addr, reg_addr, num_read)) {
                char I2C_buff[num_read+1];
                readFromI2C(chip_addr, reg_addr, num_read, I2C_buff);
                I2C_buff[num_read] = '\r';
                Serial.write((const uint8_t *)I2C_buff, num_read + 1);
            }
            break;
        case CMD_ID_WRITE:
            Serial.println("OK");
            break;
        default:
            ; //unhandled command id
    }
}


void loop()
{
    if (isPacketAvailable()) {
        respondToPacket();
    } 
}
