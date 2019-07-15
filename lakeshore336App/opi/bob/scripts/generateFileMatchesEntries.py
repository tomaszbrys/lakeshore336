# -----------------------------------------------------------------------------
# Jython - CSStudio
# -----------------------------------------------------------------------------
# LakeShore 224 - Temperature Monitoring
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
# Maximum number of file matches is 50
# -----------------------------------------------------------------------------
MAX_FILE_MATCHES = 50

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
        # get the value of trigger PV again, just for guarantee
        trigger = PVUtil.getInt(pvs[0])
        # only act, writing the new curve-query, if the trigger is '1'
        if trigger:
            # pvs[0]: loc://generateFileMatchesEntries
            # reseting the trigger value
            pvs[0].setValue(0)
            # -----------------------------------------------------------------------------
            # Input PVs
            # -----------------------------------------------------------------------------
            # pv0 = PVUtil.getString(pvs[0])
            # Reading wave-form from PV
            # $(PREFIX):CurveFile:PatternMatches
            #waveFormData = PVUtil.getTable(pvs[1])
            try:
                waveFormData = PVUtil.getStringArray(pvs[1])
            except:
                waveFormData = []
            #logger.info("waveFormData: %s" % str(waveFormData))

            # -----------------------------------------------------------------------------
            # Fill in file names according to waveform
            # -----------------------------------------------------------------------------
            # first, clean the names...
            for idx in range(MAX_FILE_MATCHES):
                pvs[idx+2].setValue("")
                #logger.info("PV value(clean): %s" % str(PVUtil.getString(pvs[idx+2])))

            for idx, data in enumerate(waveFormData):
                fileName = str(data)
                #logger.info("data: %s" % fileName)
                if fileName:
                    pvs[idx+2].setValue(fileName)
                    #logger.info("PV value: %s" % str(PVUtil.getString(pvs[idx+2])))
                else:
                    # the waveform has some trash at the end... avoid to process them at the first 'blank' name...
                    break

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
            embedded_width  = 260
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
                # forcing a 'reload'... yes, I know...
                #embedded.setPropertyValue("file", "")
                embedded.setPropertyValue("file", "curve_matches_template.bob")
                return embedded

            #display = widget.getDisplayModel()
            # coordinates of where the headers stop
            startX = 0
            startY = 0
            # resolution of display
            resX = 800
            resY = 600
            for i in range(MAX_CURVE_NAMES):
                x = startX
                y = startY + (embedded_height * (i))
                instance = createInstance(x, y, {'FILE_IDX':str(i+1)})
                display.runtimeChildren().addChild(instance)
    except Exception as e:
        logger.warning("Error! %s " % str(e))

# -----------------------------------------------------------------------------
# calling the main procedure
# -----------------------------------------------------------------------------
# get the value of trigger PV
trigger = PVUtil.getInt(pvs[0])
if trigger:
    sleep(0.2)              # this was necessary because more than one procedure were being started, probably due to the period of scan of CSStudio thread
    generatorProcedure()
