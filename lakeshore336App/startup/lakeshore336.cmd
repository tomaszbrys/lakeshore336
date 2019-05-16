#@field IPADDR
#@type STRING
#IP or hostname of the TCP endpoint.
#
#@field PREFIX
#@type STRING
#Prefix for EPICS PVs.
#
#@field REQUIRE_lakeshore336_PATH
#@runtime YES

#epicsEnvSet(IPPORT, "7777")


require pvaSrv,0+
require recsync,1.0+

#Specifying the TCP endpoint and port name
drvAsynIPPortConfigure("$(PREFIX)-asyn-port", "$(IPADDR):7777")
 
#Load your database defining the EPICS records
dbLoadTemplate(lakeshore336.substitutions, "P=$(PREFIX), PORT=$(PREFIX)-asyn-port, ADDR=7777")

#Configure file access
drvAsynFileConfigure("$(PREFIX)-calib-files", "$(REQUIRE_lakeshore336_PATH)/misc", 15000)

#Load your database defining the EPICS records
dbLoadRecords(lakeshore336_curve_management.db, "P=$(PREFIX), ASYNPORT=$(PREFIX)-asyn-port, ASYNCALIBPORT=$(PREFIX)-calib-files")

#Start calibration curve uploader
seq install_curve("P=$(PREFIX)")

##SNL callback
##Not yet put this in the substitution file...Can it be put in substitutions?
##Maybe good to have it here with teh SNL stuff..
## P for name and CHANNEL, setCHANNEL, sigCHANNEL for different numbering ...

seq callback, "name=1, P=$(PREFIX), sigCHANNEL=0, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=1, CHANNEL=1"
seq callback, "name=2, P=$(PREFIX), sigCHANNEL=1, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=2, CHANNEL=2"
seq callback, "name=3, P=$(PREFIX), sigCHANNEL=2, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=3, CHANNEL=3"
seq callback, "name=4, P=$(PREFIX), sigCHANNEL=3, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=4, CHANNEL=4"

startPVAServer
