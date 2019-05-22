# -----------------------------------------------------------------------------
# Jython - CSStudio
# -----------------------------------------------------------------------------
# Updating PVs to show Temperature or Voltage depending on user's choice
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# WP12 - douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil

# -----------------------------------------------------------------------------
# class objects
# -----------------------------------------------------------------------------
logger = ScriptUtil.getLogger()

# -----------------------------------------------------------------------------
# Assigning PVs
# -----------------------------------------------------------------------------
selection = PVUtil.getInt(pvs[0])

# -----------------------------------------------------------------------------
# Assigning text component objects to be used when updating the PV Names
# -----------------------------------------------------------------------------
# getting the current display
display = widget.getDisplayModel()
macros  = display.getPropertyValue("macros")
logger.config("prefix: %s" % str(macros.getValue('PREFIX')))
# -----------------------------------------------------------------------------
txtxRDGA  = display.runtimeChildren().getChildByName('txtxRDGA')
txtxRDGC1 = display.runtimeChildren().getChildByName('txtxRDGC1')
txtxRDGC2 = display.runtimeChildren().getChildByName('txtxRDGC2')
txtxRDGC3 = display.runtimeChildren().getChildByName('txtxRDGC3')
txtxRDGC4 = display.runtimeChildren().getChildByName('txtxRDGC4')
txtxRDGC5 = display.runtimeChildren().getChildByName('txtxRDGC5')

txtxRDGB  = display.runtimeChildren().getChildByName('txtxRDGB')
txtxRDGD1 = display.runtimeChildren().getChildByName('txtxRDGD1')
txtxRDGD2 = display.runtimeChildren().getChildByName('txtxRDGD2')
txtxRDGD3 = display.runtimeChildren().getChildByName('txtxRDGD3')
txtxRDGD4 = display.runtimeChildren().getChildByName('txtxRDGD4')
txtxRDGD5 = display.runtimeChildren().getChildByName('txtxRDGD5')


logger.config("User selected: %s" % str(selection))
if selection == 0:          # Temperature (K)
    txtxRDGA.setPropertyValue('pv_name', '%s:KRDGA' % str(macros.getValue('PREFIX')))
    txtxRDGC1.setPropertyValue('pv_name', '%s:KRDGC1' % str(macros.getValue('PREFIX')))
    txtxRDGC2.setPropertyValue('pv_name', '%s:KRDGC2' % str(macros.getValue('PREFIX')))
    txtxRDGC3.setPropertyValue('pv_name', '%s:KRDGC3' % str(macros.getValue('PREFIX')))
    txtxRDGC4.setPropertyValue('pv_name', '%s:KRDGC4' % str(macros.getValue('PREFIX')))
    txtxRDGC5.setPropertyValue('pv_name', '%s:KRDGC5' % str(macros.getValue('PREFIX')))

    txtxRDGB.setPropertyValue('pv_name', '%s:KRDGB' % str(macros.getValue('PREFIX')))
    txtxRDGD1.setPropertyValue('pv_name', '%s:KRDGD1' % str(macros.getValue('PREFIX')))
    txtxRDGD2.setPropertyValue('pv_name', '%s:KRDGD2' % str(macros.getValue('PREFIX')))
    txtxRDGD3.setPropertyValue('pv_name', '%s:KRDGD3' % str(macros.getValue('PREFIX')))
    txtxRDGD4.setPropertyValue('pv_name', '%s:KRDGD4' % str(macros.getValue('PREFIX')))
    txtxRDGD5.setPropertyValue('pv_name', '%s:KRDGD5' % str(macros.getValue('PREFIX')))
elif selection == 1:        # Temperature (C)
    txtxRDGA.setPropertyValue('pv_name', '%s:CRDGA' % str(macros.getValue('PREFIX')))
    txtxRDGC1.setPropertyValue('pv_name', '%s:CRDGC1' % str(macros.getValue('PREFIX')))
    txtxRDGC2.setPropertyValue('pv_name', '%s:CRDGC2' % str(macros.getValue('PREFIX')))
    txtxRDGC3.setPropertyValue('pv_name', '%s:CRDGC3' % str(macros.getValue('PREFIX')))
    txtxRDGC4.setPropertyValue('pv_name', '%s:CRDGC4' % str(macros.getValue('PREFIX')))
    txtxRDGC5.setPropertyValue('pv_name', '%s:CRDGC5' % str(macros.getValue('PREFIX')))

    txtxRDGB.setPropertyValue('pv_name', '%s:CRDGB' % str(macros.getValue('PREFIX')))
    txtxRDGD1.setPropertyValue('pv_name', '%s:CRDGD1' % str(macros.getValue('PREFIX')))
    txtxRDGD2.setPropertyValue('pv_name', '%s:CRDGD2' % str(macros.getValue('PREFIX')))
    txtxRDGD3.setPropertyValue('pv_name', '%s:CRDGD3' % str(macros.getValue('PREFIX')))
    txtxRDGD4.setPropertyValue('pv_name', '%s:CRDGD4' % str(macros.getValue('PREFIX')))
    txtxRDGD5.setPropertyValue('pv_name', '%s:CRDGD5' % str(macros.getValue('PREFIX')))
else:                       # Voltage
    txtxRDGA.setPropertyValue('pv_name', '%s:SRDGA' % str(macros.getValue('PREFIX')))
    txtxRDGC1.setPropertyValue('pv_name', '%s:SRDGC1' % str(macros.getValue('PREFIX')))
    txtxRDGC2.setPropertyValue('pv_name', '%s:SRDGC2' % str(macros.getValue('PREFIX')))
    txtxRDGC3.setPropertyValue('pv_name', '%s:SRDGC3' % str(macros.getValue('PREFIX')))
    txtxRDGC4.setPropertyValue('pv_name', '%s:SRDGC4' % str(macros.getValue('PREFIX')))
    txtxRDGC5.setPropertyValue('pv_name', '%s:SRDGC5' % str(macros.getValue('PREFIX')))

    txtxRDGB.setPropertyValue('pv_name', '%s:SRDGB' % str(macros.getValue('PREFIX')))
    txtxRDGD1.setPropertyValue('pv_name', '%s:SRDGD1' % str(macros.getValue('PREFIX')))
    txtxRDGD2.setPropertyValue('pv_name', '%s:SRDGD2' % str(macros.getValue('PREFIX')))
    txtxRDGD3.setPropertyValue('pv_name', '%s:SRDGD3' % str(macros.getValue('PREFIX')))
    txtxRDGD4.setPropertyValue('pv_name', '%s:SRDGD4' % str(macros.getValue('PREFIX')))
    txtxRDGD5.setPropertyValue('pv_name', '%s:SRDGD5' % str(macros.getValue('PREFIX')))
