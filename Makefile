SRC=location-checker-applet.py
APPLET=org.mate.applets.LocationCheckerApplet.mate-panel-applet
SERVICE=org.mate.panel.applet.LocationCheckerAppletFactory.service

export SRC_TARGET=/usr/share/mate-applets/location-checker/$(SRC)
APPLET_TARGET=/usr/share/mate-panel/applets/$(APPLET)
SERVICE_TARGET=/usr/share/dbus-1/services/$(SERVICE)

install:
	@mkdir -p `dirname $(SRC_TARGET)`
	@cp $(SRC) $(SRC_TARGET)
	@envsubst < $(APPLET) > $(APPLET_TARGET)
	@envsubst < $(SERVICE) > $(SERVICE_TARGET)

uninstall:
	@rm -rf `dirname $(SRC_TARGET)`
	@rm $(APPLET_TARGET)
	@rm $(SERVICE_TARGET)
