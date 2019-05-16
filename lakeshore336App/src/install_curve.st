program install_curve("P, CurvePrefix=File")

option +r;
option +d;

%%#include <stdio.h>
%%#include <errlog.h>


int     NumBreakpoints;
assign  NumBreakpoints     to "{P}:Curve{CurvePrefix}:NumBreakpoints";

int     Breakpoints_NORD;
assign  Breakpoints_NORD   to "{P}:Curve{CurvePrefix}:Breakpoints.NORD";

double  Breakpoints[600];
assign  Breakpoints        to "{P}:Curve{CurvePrefix}:Breakpoints";

int     Install;
assign  Install            to "{P}:Curve{CurvePrefix}:Install";
monitor Install;

int     DataFormat;
assign  DataFormat         to "{P}:Curve{CurvePrefix}:DataFormat";

int     FileFormat;
assign  FileFormat         to "{P}:Curve{CurvePrefix}:Type.RVAL";

int     InstallEntry;
assign  InstallEntry       to "{P}:Curve{CurvePrefix}:InstallEntry";

int     InstallIndex;
assign  InstallIndex       to "{P}:Curve{CurvePrefix}:iInstallIndex";

int     InstallHeader;
assign  InstallHeader      to "{P}:Curve{CurvePrefix}:iInstallHeader.PROC";

double  InstallSensorUnit;
assign  InstallSensorUnit  to "{P}:Curve{CurvePrefix}:iInstallSensorUnit";

double  InstallKelvin;
assign  InstallKelvin      to "{P}:Curve{CurvePrefix}:iInstallKelvin";

int     InstallPoint;
assign  InstallPoint       to "{P}:Curve{CurvePrefix}:iInstallPoint.PROC";

int     PointInstalled;
assign  PointInstalled     to "{P}:Curve{CurvePrefix}:iPointInstalled";
monitor PointInstalled;

int     InstallStatus;
assign  InstallStatus      to "{P}:Curve{CurvePrefix}:InstallStatus";

string  CurveName;
assign  CurveName;



ss CURVE
{
	state init
	{
		when ()
		{
			Install = 0;
			pvPut(Install, SYNC);
		} state waitForRequest
	}


	state waitForRequest
	{
		when (Install)
		{
			InstallStatus = 0;

			pvPut(InstallStatus, SYNC);
			pvGet(DataFormat, SYNC);
			pvGet(FileFormat, SYNC);
			pvGet(NumBreakpoints, SYNC);
			pvGet(Breakpoints_NORD, SYNC);
		} state checkFormat
	}


	state checkFormat
	{
		when (DataFormat > 4 || DataFormat < 1)
		{
			InstallStatus = 2;
			errlogPrintf("Curve Install: Unsupported curve data format\n");
		} state failedInstall

		when (FileFormat < 1 || FileFormat > 2)
		{
			InstallStatus = 2;
			errlogPrintf("Curve Install: Unsupported curve file format\n");
		} state failedInstall

		when ()
		{
		} state checkBreakpoints
	}


	state checkBreakpoints
	{
		when (FileFormat == 1 && NumBreakpoints != Breakpoints_NORD / 3)
		{
			InstallStatus = 3;
			errlogPrintf("Curve Install: Inconsistent number of breakpoints\n");
		} state failedInstall

		when (FileFormat == 2 && NumBreakpoints != Breakpoints_NORD / 2)
		{
			InstallStatus = 3;
			errlogPrintf("Curve Install: Inconsistent number of breakpoints\n");
		} state failedInstall

		when ()
		{
		} state initializeInstall
	}


	state initializeInstall
	{
		when ()
		{
			InstallStatus = 0;
			pvPut(InstallStatus, ASYNC);

			InstallIndex   = 1;
			pvPut(InstallIndex, ASYNC);

			PointInstalled = 0;
			pvPut(PointInstalled, ASYNC);

			pvGet(Breakpoints, ASYNC);
			pvGet(InstallEntry, SYNC);
		} state waitForPVCompletion
	}


	state waitForPVCompletion
	{
		when (
			pvPutComplete(PointInstalled) &&
			pvPutComplete(InstallIndex) &&
			pvGetComplete(NumBreakpoints) &&
			pvGetComplete(Breakpoints))
		{
		} state installHeader
	}


	state installHeader
	{
		when ()
		{
#ifdef DEBUG
errlogPrintf("Curve Install: Installing header...\n");
#endif
			InstallHeader = 1;
			pvPut(InstallHeader, SYNC);

			/*
			 * Retrieve status information
			 */
			pvGet(InstallHeader, SYNC);

			InstallIndex = 0;
			//pvPut(InstallIndex) left out intentionally
		} state checkHeader
	}


	state checkHeader
	{
		when (pvStatus(InstallHeader) != pvStatOK || pvSeverity(InstallHeader) != pvSevrOK)
		{
			InstallStatus = 4;
			errlogPrintf("Curve Install: Header installation failed!\n");
		} state failedInstall

		when ()
		{
#ifdef DEBUG
			if (FileFormat == 1)
				errlogPrintf("Curve Install: Installing .340 format\n");
			else if (FileFormat == 2)
				errlogPrintf("Curve Install: Installing .curve format\n");
#endif
		} state installBreakpoints
	}


	state installBreakpoints
	{
		when (pvStatus(InstallPoint) != pvStatOK || pvSeverity(InstallPoint) != pvSevrOK)
		{
			InstallStatus = 5;
			errlogPrintf("Curve Install: Installation failed!\n");
		} state failedInstall

		when (InstallIndex < NumBreakpoints)
		{
			if (FileFormat == 1)
			{
				InstallSensorUnit = Breakpoints[InstallIndex * 3 + 1];
				InstallKelvin     = Breakpoints[InstallIndex * 3 + 2];
			}
			else if (FileFormat == 2)
			{
				InstallSensorUnit = Breakpoints[InstallIndex * 2];
				InstallKelvin     = Breakpoints[InstallIndex * 2 + 1];
			}

			++InstallIndex;

			pvPut(InstallIndex, SYNC);
			pvPut(InstallSensorUnit, SYNC);
			pvPut(InstallKelvin, SYNC);

#ifdef DEBUG
errlogPrintf("CRVPT %d,%d,%f,%f\n", InstallEntry, InstallIndex, InstallSensorUnit, InstallKelvin);
#endif

			pvPut(InstallPoint, SYNC);

			/*
			 * For some reason monitor is not enough
			 */
			pvGet(PointInstalled, SYNC);
		} state waitForBreakpointCompletion

		when (InstallIndex >= NumBreakpoints)
		{
#ifdef DEBUG
errlogPrintf("Curve Install: Installed\n");
#endif
		} state installed
	}


	state waitForBreakpointCompletion
	{
		when (PointInstalled == InstallIndex)
		{
			/*
			 * Retrieve status information
			 */
			pvGet(InstallPoint, SYNC);
		} state installBreakpoints
	}


	state failedInstall
	{
		when ()
		{
			pvPut(InstallStatus);
		} state init
	}


	state installed
	{
		when ()
		{
			char curvenamepv[80];
			snprintf(curvenamepv, sizeof(curvenamepv), "%s:Curve%d:Name", macValueGet("P"), InstallEntry);
			pvAssign(CurveName, curvenamepv);

			InstallStatus = 1;
			pvPut(InstallStatus);
		} state rereadCurveName
	}


	state rereadCurveName
	{
		when (delay(5))
		{
		} state init

		when (pvConnected(CurveName))
		{
			CurveName[0] = '\0';
			pvPut(CurveName);
		} state init
	}
}
