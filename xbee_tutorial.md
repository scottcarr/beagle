#XBee Tips

XBee is basically serial over wireless.

If you hook the [XBee Explorer](https://www.sparkfun.com/products/8687) to
your USB port you can talk to the XBee throught a serial port program like
[CoolTerm](http://www.macupdate.com/app/mac/31352/coolterm) or 
[RealTerm](http://realterm.sourceforge.net/).

##Some gotchas

Plugging the USB connector into the Arduino Fio makes many of the LEDs come
on, but it wasn't actually powering up all the way for me.  I had to use the
[FTDI to USB cable](https://www.sparkfun.com/products/9717) to get it to work
correctly.  This was with no battery connected.  It might work normally with a 
battery.

##Configuration

To configure the XBee radio, you put it in configuration mode by sending '+++'
with no carriage return or line feed after.  It should respond 'OK'.  I'm not
sure what happens if you send 3 plus signs in a row by accident, probably diaster
happens.

##Wireless programming

Wireless programming works just like regular programming if the XBee radios
are setup correctly.  I followed 
[this tutorial](http://arduino.cc/en/Main/ArduinoBoardFioProgramming)
The only weird thing is the jumper between RTS and DIO3.  This is a 'hack'
to get the wireless reprogramming to work.  The DIO3 on the programmer side
is sent to the Fio side and since it's tied to RTS, DI03 goes active whenever
the programmer sends data.  DIO3 is tied to reset on the FIO side, so it resets
the Fio whenever it sends it a message.  We might need to unjumper RTS/DIO3
for operation and use an actual software controlled digital output.

------------------------------------------

Other resources:

[Sparkfun Xbee product page](https://www.sparkfun.com/products/8665)
