################################################################
### requires
require stream,      2.8.8
require lakeshore336,2.0.3
require iocStats,    ae5d083
require asynfile,    0.0.2

require calc,       3.7.1
require sequencer,  2.2.6

### lakeshore336 (ls1)
#epicsEnvSet("LOCATION",             "Utgard:10.0.7.141")
epicsEnvSet("LOCATION",             "Utgard:10.0.7.244")
#epicsEnvSet("IPADDR",               "10.0.7.141")
epicsEnvSet("IPADDR",               "10.0.7.244")
#epicsEnvSet("SYS",                  "UTG-SEE-TEFI:")
epicsEnvSet("SYS",                  "UTG-SEE-TEFI:")
#epicsEnvSet("DEV",                  "Tctrl-LS336-002")
epicsEnvSet("DEV",                  "Tmt-LS336-02")
epicsEnvSet("PREFIX",               "$(SYS)$(DEV)")
epicsEnvSet("IPPORT",               "7777")
#epicsEnvSet("IOCNAME",             "$(SYS)LS336-002")
epicsEnvSet("IOCNAME",              "LS336-002")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(lakeshore336_DIR)db/")

### load all db's
iocshLoad("$(lakeshore336_DIR)lakeshore336.iocsh", "PREFIX=$(PREFIX), IPADDR=$(IPADDR), IPPORT=$(IPPORT)")
iocshLoad("$(iocStats_DIR)/iocStats.iocsh")

### install SNL curves
seq install_curve, "P=$(PREFIX), CurvePrefix=File"

iocInit
