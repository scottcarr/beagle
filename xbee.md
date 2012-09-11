#My investigation into XBee

XBee is basically a "wireless serial bus".  It just gives you a way to transport ASCII characters.  It's up to you to define the protocol (which gives you the flexibility of designing any protocol you wish.)

There are two ways of connecting the XBee to the beagle:

1. USB, using the [XBee explorer](https://www.sparkfun.com/products/8687)
2. Directly to one of the beagle's available 
[UARTs](http://en.wikipedia.org/wiki/Universal_asynchronous_receiver/transmitter)

Both ways are just different physical implementations that accomplish the same 
thing (bi-directional serial communication).

I was favoring #2 because the USB port is also how you get a console connection 
to the beagle, and AFAIK, the other UARTs aren't used for anything.

Directly connecting the XBee to the beagle entails:

1. Converting the XBee's 0.2mm spaced header to standard 0.1mm 
(we bought a [breakout board](https://www.sparkfun.com/products/8276)  for this)
2. Connecting the result to the beagleboard proto cape
3. Wiring the proto cape to expose the desired UART pins (Rx, Tx, RTS, CTS, etc)

I should be able to do those 3 pretty easily once the parts arrive.

##The remaining questions are:

###How are the beagle's UARTs exposed in Angstrom Linux?  
My guess would be they're under /dev and we can just talk to them via file read/write)
###What configuration (if any) do we need to do to get the UART to talk to the XBee?  
bit rate, parity, etc
