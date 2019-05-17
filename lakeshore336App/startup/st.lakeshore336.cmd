epicsEnvSet(IPPORT, "7777")
epicsEnvSet(PORTNAME, "ls336")
epicsEnvSet(IPADDR, "10.0.7.141")
epicsEnvSet(PREFIX, "ls1")

require lakeshore336,  2.0.2
require recsync,       1.0+
require asyn,          4.33.0
require calc,          3.7.1
require sequencer,     2.2.6
require stream,        2.8.8
require asynfile,      0.0.1

#Load your IOC shell which will load all databases
iocshLoad("$(lakeshore336_DIR)lakeshore336.iocsh", "PREFIX=$(PREFIX), IPADDR=$(IPADDR), IPPORT=$(IPPORT)")

