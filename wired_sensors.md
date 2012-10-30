#Wired Sensors

I'm not sure if this is already written down somewhere, but these are the sensors on the instrumented turbine:

[accelerometers on the blades](http://www.silicondesigns.com/ds/ds2460.html) (the 2460-050 part #)

[tachometer](http://www.bannerengineering.com/en-US/support/partref/28155#specstabcontent)

[accelerometer on the hub](http://www.pcb.com/spec_sheet.asp?model=3713B1150G&item_id=14320)

I couldn't find a part number for the anemometer.

If we wanted a reproduce the same setup on the other turbine we'd need:

A power suppy 8-32V with enough current to drive all the sensors.  They 
are all pretty low current, so that shouldn't be a big problem.

A circuit for the tach to switch.  It's a PNP (or NPN) transistor.

How is the output power being measured?  There has been talk of changing/improving
the power measurement, but I'm not sure how high priority that is.

