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
    # This Python script is attached to a display and triggered by loc://generateCurveValuePlotEntries(1)
    # to execute once when the display is loaded.
    # -----------------------------------------------------------------------------
    try:
        # -----------------------------------------------------------------------------
        # Input PVs
        # -----------------------------------------------------------------------------
        # pv0 = PVUtil.getString(pvs[0])                        # trigger
        pvCurveValuePlotX = PVUtil.getString(pvs[1])          # loc://curveValuePlotX(0)
        pvCurveValuePlotY = PVUtil.getString(pvs[2])          # loc://curveValuePlotY(0)

        # -----------------------------------------------------------------------------
        # Loading macros defined for the current display
        # -----------------------------------------------------------------------------
        display         = widget.getDisplayModel()
        old_macros      = display.getEffectiveMacros()
        prefix          = old_macros.getValue('PREFIX')         # UTG-SEE-FLUC:Tmt-LS224-01

        # ---------------------------------------------------------------------
        # Local objects
        # ---------------------------------------------------------------------
        curveValuesX = []       # UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.B (temperatures)
        curveValuesY = []       # UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.A (units)

        for index in range(1, 201):
            # obtain the read value of units, temperature for one data-point (from 1 until 200)...
            #     > the PV is something like: 
            #           UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.A
            #           UTG-SEE-FLUC:Tmt-LS224-01:Curve:DP<999>.B
            #     > generated from macros: $(PREFIX):Curve:DP<index>.A and $(PREFIX):Curve:DP<index>.B
            unitPvName = "%s:Curve:DP%d.A" % (prefix, index)
            tempPvName = "%s:Curve:DP%d.B" % (prefix, index)
            pvEpicsUnit = 0.0
            pvEpicsTemp = 0.0
            try:
                # getting PV values from names
                pvEpicsUnit = PVUtil.getDouble(PVFactory.getPV(unitPvName))
                pvEpicsTemp = PVUtil.getDouble(PVFactory.getPV(tempPvName))
                #logger.info("pvEpicsUnit: %s, %f" % (unitPvName, pvEpicsUnit))
                #logger.info("pvEpicsTemp: %s, %d" % (tempPvName, pvEpicsTemp))
                # adding the values to the tables...
                if (pvEpicsTemp and pvEpicsUnit):
                    curveValuesX.append(pvEpicsTemp)
                    curveValuesY.append(pvEpicsUnit)
                    #logger.info("curveValuesX: %s" % str(curveValuesX))
                    #logger.info("curveValuesY: %s" % str(curveValuesY))
            except:
                logger.warning("Error trying to read %s or %s" % (unitPvName, tempPvName))
        # setting XYPlot PVs with the arrays...
        pvs[1].setValue(curveValuesX)
        pvs[2].setValue(curveValuesY)

    except Exception as e:
        logger.warning("Error! %s " % str(e))

# -----------------------------------------------------------------------------
# calling the main procedure
# -----------------------------------------------------------------------------
sleep(0.2)              # this was necessary because more than one procedure were being started, probably due to the period of scan of CSStudio thread
generatorProcedure()
