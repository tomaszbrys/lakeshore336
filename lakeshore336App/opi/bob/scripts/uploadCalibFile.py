# -----------------------------------------------------------------------------
# Jython - CSStudio
# -----------------------------------------------------------------------------
# Lakeshore224 - UploadCalibFile
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# WP12 - douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
#from pvaccess import BOOLEAN, BYTE, UBYTE, SHORT, USHORT, INT, UINT, LONG, ULONG, FLOAT, DOUBLE, STRING, PvObject, PvaServer

import sys, time, datetime, os

from time import sleep
from array import array
from jarray import zeros

from ftplib import FTP, FTP_TLS

# -----------------------------------------------------------------------------
# class objects
# -----------------------------------------------------------------------------
logger = ScriptUtil.getLogger()

# -----------------------------------------------------------------------------
# Default IOC user and password;
# I know... should think about how to login without expose the password...
# -----------------------------------------------------------------------------
LOGIN_USER   = "iocuser"
LOGIN_PASSWD = "vaha23neca"

# -----------------------------------------------------------------------------
# procedures
# -----------------------------------------------------------------------------
def uploadCalibFile():
    try:
        # ---------------------------------------------------------------------
        # logical representation of PVs
        # ---------------------------------------------------------------------
        triggerCalibFile    = PVUtil.getInt(pvs[0])
        localCalibFile      = PVUtil.getString(pvs[1])

        # -----------------------------------------------------------------------------
        # Getting the macros that should have information of remote server
        # -----------------------------------------------------------------------------
        display             = widget.getDisplayModel()
        macros              = display.getEffectiveMacros()
        # 
        iocServerIp       = macros.getValue('IOC_SERVER_IP')
        remoteCalibPath   = macros.getValue('CALIB_FILES_REMOTE_PATH')
        #logger.info("iocServerIp: %s" % iocServerIp)
        #logger.info("remoteCalibPath: %s" % remoteCalibPath)
        # 
        if os.path.isfile(localCalibFile):
            now = datetime.datetime.now()
            timeStamp = now.strftime('%Y%m%dT%H%M%S')
            logger.info(localCalibFile)
            #ftpObject = FTP(iocServerIp, LOGIN_USER, LOGIN_PASSWD)                    # connect to host, default port
            ftpObject = FTP(iocServerIp)                    # connect to host, default port
            ftpObject.login(LOGIN_USER, LOGIN_PASSWD)       # iocuser; known password;
            #logger.info("connected...")
            # 
            #ftpObject.retrlines('LIST')     # list directory contents
            # set remote directory
            ftpObject.cwd(remoteCalibPath)
            #logger.info("changed directory...")
            # sendint the file
            fileObject = open(localCalibFile, "rb")
            # parse the input file (with full path) to rename it including timestamp...
            # expecting something like this:
            #       e.g.: '/home/douglasbeniz/ESS/SampleEnvironmentGroup/Lakeshore224/LS224-Utgard/Curves/CurveHandler/6-PT-100.340'
            fileName = localCalibFile[localCalibFile.rfind('/')+1:]
            if fileName.find('.') > 0:
                # expecting something like this:
                #       e.g.: '6-PT-100.340'
                # and should transform in something like this:
                #       e.g.: '6-PT-100_20190522T190240.340'
                newFileName = '%s_%s.%s' % (fileName[:fileName.rfind('.')], timeStamp, fileName[fileName.rfind('.')+1:])
            else:
                newFileName = '%s_%s' % (fileName, timeStamp)
            #logger.info("newFileName: %s" % newFileName)
            # send the file...
            ftpObject.storbinary('STOR %s' % newFileName, fileObject) 
            # logger.info("file copied!")
            # close the file
            fileObject.close()
            # close the connection
            ftpObject.quit()

    except Exception as e:
        logger.warning("Error! %s " % str(e))

# -----------------------------------------------------------------------------
# calling the main procedure
# -----------------------------------------------------------------------------
sleep(0.2)              # this was necessary because more than one procedure were being started, probably due to the period of scan of CSStudio thread
uploadCalibFile()