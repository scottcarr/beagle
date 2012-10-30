DOC_DIR = /home/wind-wiki/htdocs/doc/

all: I2C_accel_gyro_combo.html xbee.html xbee_tips.html uart.html fio.html \
	sd.html sd_logger_app.html experiment10252012.html wired_sensors.html

I2C_accel_gyro_combo.html:
	markdown I2C_accel_gyro.md > $(DOC_DIR)I2C_accel_gyro_combo.html

xbee.html:
	markdown xbee.md > $(DOC_DIR)xbee.html

xbee_tips.html:
	markdown xbee_tutorial.md > $(DOC_DIR)xbee_tips.html

fio.html:
	cp fio.jpg $(DOC_DIR)fio.jpg
	markdown fio.md > $(DOC_DIR)fio.html

uart.html:
	markdown UART.md > $(DOC_DIR)uart.html
	cp beaglexbee.jpg $(DOC_DIR)beaglexbee.jpg

sd_logger_app.html:
	markdown sd_logger.md > $(DOC_DIR)sd_logger_app.html
	cp accel.png $(DOC_DIR)accel.png
	cp gyro.png $(DOC_DIR)gyro.png

sd.html:
	markdown sd.md > $(DOC_DIR)sd.html

experiment10252012.html:
	markdown experiments10252012/log.md > $(DOC_DIR)experiment10252012.html
	
wired_sensors.html:
	markdown wired_sensors.md > $(DOC_DIR)wired_sensors.html

clean:
	rm $(DOC_DIR)xbee.html $(DOC_DIR)I2C_accel_gyro_combo.html
