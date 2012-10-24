#Fio SD card setup

See here for [SD card pinout](http://www.interfacebus.com/Secure_Digital_Card_Pinout.html)

The Fio pins are labeled on the board.  All of these pins are digital.

<table>
<tr>    <td>Fio Pin</td>    <td>SD Card Pin</td>    <td>Description</td> </tr>
<tr>    <td>10</td>    <td>1</td>    <td>SS</td> </tr>
<tr>    <td>11</td>    <td>2</td>    <td>MOSI</td> </tr>
<tr>    <td>12</td>    <td>7</td>    <td>MISO</td> </tr>
<tr>    <td>13</td>    <td>5</td>    <td>SCK</td> </tr>
<tr>    <td>3V3</td>    <td>4</td>    <td>Power</td> </tr>
<tr>    <td>GND</td>    <td>3</td>    <td>Ground</td> </tr>
</table>

The Arduino has an [SD card library](http://www.interfacebus.com/Secure_Digital_Card_Pinout.html)

The SD card should be formated FAT16 or FAT32.

Example code:

    int chipSelect = 10;
    pinMode(chipSelect, OUTPUT);
    if(!SD.begin(chipSelect)) {
        while (1) {
            Serial.println("SD card failed.");
        }
    } else {
        Serial.println("SD card initialized.");
    }
    if (SD.exists("data.csv")) {
        SD.remove("data.csv"); // get rid of out data
    }
    data = SD.open("data.csv", FILE_WRITE);
