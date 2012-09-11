DOC_DIR = /home/wind-wiki/htdocs/doc/

all: I2C_accel_gyro_combo.html xbee.html

I2C_accel_gyro_combo.html:
	markdown I2C_accel_gyro.md > $(DOC_DIR)I2C_accel_gyro_combo.html

xbee.html:
	markdown xbee.md > $(DOC_DIR)xbee.html

clean:
	rm $(DOC_DIR)xbee.html $(DOC_DIR)I2C_accel_gyro_combo.html
