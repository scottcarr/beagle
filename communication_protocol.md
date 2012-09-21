#Communication Protocol - DRAFT

My current thinking is that it's best to make everything as general as possible,
since the design in development.

Since the sensors we're using currently are I2C, I propose to map the I2C
interface onto XBee. For that, we need two commands, read and write.

###I2C Write command format

<table>
    <tr>
        <td>Command ID (byte)</td>
        <td>Chip Address (byte)</td>
        <td>Chip register Address (byte)</td>
        <td>Value (byte)</td>
    </tr>
    <tr>
        <td>0x01</td>
        <td>Address of chip on I2C bus (0x00 - 0x7F)</td>
        <td>Address of register (on the chip) to write</td>
        <td>Value to write</td>
    </tr>
<\table>

Each field is a byte.  They are sent sequentially and followed by a carriage
return (0x0D in ASCII).

For example, the command:
<table>
    <tr>
        <td>Command ID</td>
        <td>Chip Address</td>
        <td>Chip register Address</td>
        <td>Value</td>
    </tr>
    <tr>
        <td>0x01</td>
        <td>0x53</td>
        <td>0x2a</td>
        <td>0x11</td>
    </tr>
</table>

Yields 01 53 2a 11 0A

Support for multi-byte writes may be added as needed.

###I2C Read command format

<table>
    <tr>
        <td>Command ID (byte)</td>
        <td>Chip Address (byte)</td>
        <td>Chip register Address (byte)</td>
        <td>Number of bytes to read (byte)</td>
    </tr>
    <tr>
        <td>0x02</td>
        <td>0x53</td>
        <td>0x2a</td>
        <td>0x01</td>
    </tr>
<\table>

Again, these fields are bytes and are followed by a carriage return.

Example command:

<table>
    <tr>
        <td>Command ID</td>
        <td>Chip Address</td>
        <td>Chip register Address</td>
        <td>Number of bytes to read</td>
    </tr>
    <tr>
        <td>0x02</td>
        <td>0x53</td>
        <td>0x2a</td>
        <td>0x01</td>
    </tr>
<\table>

Yields 02 53 2a 11 0A

##To do

A message that deals with multiple samples.  My current idea is that I think
the Accel/Gyro chips have a FIFO.  The can generate an interrupt when it is
nearly full.  Maybe define message that tell the Fio what to do when it gets
a certain interrupt.  Ex: "On interrupt 1, read 1024 bytes from I2C address 
0x53, address 0x10"


