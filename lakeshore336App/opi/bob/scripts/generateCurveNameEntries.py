# -----------------------------------------------------------------------------
# Jython - CSStudio
# -----------------------------------------------------------------------------
# LakeShore 336 - Temperature Monitoring
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# WP12 - douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
from org.csstudio.display.builder.model import WidgetFactory

import os, sys, time

from time import sleep
from array import array
from jarray import zeros

# -----------------------------------------------------------------------------
# Maximum number of curve names is 59
# -----------------------------------------------------------------------------
MAX_CURVE_NAMES = 59

# -----------------------------------------------------------------------------
# class objects
# -----------------------------------------------------------------------------
logger = ScriptUtil.getLogger()
# -----------------------------------------------------------------------------
# procedures
# -----------------------------------------------------------------------------
def generatorProcedure():
    #logger.info("generatorProcedure")
    # -----------------------------------------------------------------------------
    # This Python script is attached to a display
    # and triggered by loc://initial_trigger$(DID)(1)
    # to execute once when the display is loaded.
    # -----------------------------------------------------------------------------
    try:
        # -----------------------------------------------------------------------------
        # Input PVs
        # -----------------------------------------------------------------------------
        # pv0 = PVUtil.getString(pvs[0])

        # -----------------------------------------------------------------------------
        # Loading display
        # -----------------------------------------------------------------------------
        display = widget.getDisplayModel()
        #logger.info("moduleChan: %d" % int(moduleDesc[int(card_nr)].split(',')[2]))

        # -----------------------------------------------------------------------------
        # Create display:
        # -----------------------------------------------------------------------------
        # For each 'channel', add one embedded display
        # which then links to the curve_name_template.bob
        # with the macros of the device.
        embedded_width  = 280
        embedded_height = 20

        def createInstance(x, y, macros):
            embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget();
            embedded.setPropertyValue("x", x)
            embedded.setPropertyValue("y", y)
            embedded.setPropertyValue("width", embedded_width)
            embedded.setPropertyValue("height", embedded_height)
            embedded.setPropertyValue("resize", "2")
            for macro, value in macros.items():
                embedded.getPropertyValue("macros").add(macro, value)
            embedded.setPropertyValue("file", "curve_names_template.bob")
            return embedded

        #display = widget.getDisplayModel()
        # coordinates of where the headers stop
        startX = 10
        startY = 10
        # resolution of display
        resX = 800
        resY = 600
        for i in range(MAX_CURVE_NAMES):
            x = startX
            y = startY + (embedded_height * (i))
            instance = createInstance(x, y, {'CURVE':str(i+1)})
            display.runtimeChildren().addChild(instance)
    except Exception as e:
        logger.warning("Error! %s " % str(e))

# -----------------------------------------------------------------------------
# calling the main procedure
# -----------------------------------------------------------------------------
sleep(0.2)              # this was necessary because more than one procedure were being started, probably due to the period of scan of CSStudio thread
generatorProcedure()
