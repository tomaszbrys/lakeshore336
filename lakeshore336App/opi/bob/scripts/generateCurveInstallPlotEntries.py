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
from org.csstudio.display.builder.runtime.pv import PVFactory, RuntimePVFactory
from org.csstudio.display.builder.model import WidgetFactory

import os, sys, time

from time import sleep
from array import array
from jarray import zeros

# -----------------------------------------------------------------------------
# Maximum number of curve datapoints is 200
# -----------------------------------------------------------------------------
MAX_DATA_POINTS = 200

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
    # This Python script is attached to a display and triggered by loc://generatecurveInstallPlotEntries(1)
    # to execute once when the display is loaded.
    # -----------------------------------------------------------------------------
    try:
        # -----------------------------------------------------------------------------
        # Input PVs
        # -----------------------------------------------------------------------------
        # Reading wave-form from PV $(PREFIX):CurveFile:Breakpoints
        waveFormData = PVUtil.getTable(pvs[0])                  # trigger
        pvcurveInstallPlotX = PVUtil.getString(pvs[1])          # loc://curveInstallPlotX(0)
        pvcurveInstallPlotY = PVUtil.getString(pvs[2])          # loc://curveInstallPlotY(0)

        # ---------------------------------------------------------------------
        # Local objects
        # ---------------------------------------------------------------------
        curveInstallX = []       # UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.B (temperatures)
        curveInstallY = []       # UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.A (units)

        # Auxiliary variables to control all the process
        newColIdx = 0

        # Iterate over the data read from wave-form
        for data in waveFormData:
            # Debug purposes...
            # logger.info("data: %f" % data[0])
            try:
                # All data in the wave-form are a single array (1D), but the known structure
                # is a set of 3 columns: [index, units, temperatures];
                # it is necessary to artificially split the cells, three by three...
                if newColIdx == 3:
                    newColIdx = 0
                    # simply restart the column index...
                newData = 0
                if newColIdx == 0:
                    # index of datapoint, we do not use it here...
                    pass
                elif newColIdx == 1:
                    # index, use integer, so
                    valUnit = data[0]
                    #logger.info("valUnit: %f" % (valUnit))
                    curveInstallY.append(valUnit)
                else:
                    newData = data[0]
                    valTemp = int(data[0])
                    #logger.info("valTemp: %f" % (valTemp))
                    curveInstallX.append(valTemp)
                # Next column
                newColIdx += 1
            except:
                logger.warning("Error trying to read datapoint values for install_plot")

        # Adding the latest gathered row values into local PVs
        pvs[1].setValue(curveInstallX)
        pvs[2].setValue(curveInstallY)

    except Exception as e:
        logger.warning("Error! %s " % str(e))

# -----------------------------------------------------------------------------
# calling the main procedure
# -----------------------------------------------------------------------------
sleep(0.2)              # this was necessary because more than one procedure were being started, probably due to the period of scan of CSStudio thread
generatorProcedure()
