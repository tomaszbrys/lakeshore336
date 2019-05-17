require asyn,       4.33.0
### require autosave,   5.9.0
require calc,       3.7.1
### require iocStats,   ae5d083
### require pvaSrv      0.12.0  # v7 ?
### require recsync,    1.3.0
require sequencer,  2.2.6
require stream,     2.8.8
### require asynfile,   0.0.1
require lakeshore336, 2.0.2

epicsEnvSet(EPICS_CA_MAX_ARRAY_BYTES,1000000)

epicsEnvSet("IPADDR", "10.0.7.141")
epicsEnvSet("SYS", "LabS-Utgard-VIP:")
epicsEnvSet("DEV", "SES-AmpLI-1")
epicsEnvSet("PREFIX", "ls1")

#Specifying the TCP endpoint and port name
drvAsynIPPortConfigure("$(PREFIX)-asyn-port", "$(IPADDR):7777")

# Define the protocol path
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(lakeshore336_DB)")
 
#Load your database defining the EPICS records
dbLoadTemplate(lakeshore336.substitutions, "P=$(PREFIX), PORT=$(PREFIX)-asyn-port, PROTOCOL=lakeshore336.proto, ADDR=7777")

#Configure file access
# drvAsynFileConfigure("$(PREFIX)-calib-files", "$(REQUIRE_lakeshore336_PATH)/misc", 15000)

#Load your database defining the EPICS records
# dbLoadRecords(lakeshore336_curve_management.db, "P=$(PREFIX), ASYNPORT=$(PREFIX)-asyn-port, ASYNCALIBPORT=$(PREFIX)-calib-files")

#Start calibration curve uploader
# seq install_curve("P=$(PREFIX)")

##SNL callback
##Not yet put this in the substitution file...Can it be put in substitutions?
##Maybe good to have it here with teh SNL stuff..
## P for name and CHANNEL, setCHANNEL, sigCHANNEL for different numbering ...

# seq callback, "name=1, P=$(PREFIX), sigCHANNEL=0, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=1, CHANNEL=1"
# seq callback, "name=2, P=$(PREFIX), sigCHANNEL=1, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=2, CHANNEL=2"
# seq callback, "name=3, P=$(PREFIX), sigCHANNEL=2, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=3, CHANNEL=3"
# seq callback, "name=4, P=$(PREFIX), sigCHANNEL=3, SIGNAL=KRDG, SETPOINT=SETP_S, setCHANNEL=4, CHANNEL=4"

iocInit
# startPVAServer
