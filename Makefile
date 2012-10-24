DOC_DIR = /home/wind-wiki/htdocs/doc/

all: I2C_accel_gyro_combo.html xbee.html xbee_tips.html uart.html fio.html \
	sd.html sd_logger_app.html

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

sd.html:
	markdown sd.md > $(DOC_DIR)sd.html

clean:
	rm $(DOC_DIR)xbee.html $(DOC_DIR)I2C_accel_gyro_combo.html
