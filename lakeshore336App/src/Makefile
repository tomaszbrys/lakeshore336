TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = lakeshore336
# lakeshore336.dbd will be created and installed
DBD += lakeshore336.dbd

# lakeshore336.dbd will be made up from these files:
lakeshore336_DBD += base.dbd

# Include dbd files from all support applications:
#lakeshore336_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#lakeshore336_LIBS += xxx

# lakeshore336_registerRecordDeviceDriver.cpp derives from lakeshore336.dbd
lakeshore336_SRCS += lakeshore336_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
lakeshore336_SRCS_DEFAULT += lakeshore336Main.cpp
lakeshore336_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#lakeshore336_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
lakeshore336_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

