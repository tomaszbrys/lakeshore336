program callback

// State machine that checks if the value is within a signal and time window
// First the signal need to reach the value, then stay within the threshold values
// until the settling time has passed. If it has not done this before timeout
// time has passed a timout will be flagged but it will not interrupt anything.
// if temp is eventually within temp and time win ready will be set.


// IMPORTANT making the code reentrant enabling having multiple instances of it!
option +r;

//************* assign variables to PVs ******

// The parameter to add a callback to.
// Macros allowing to set which signal in the .cmd file

float value;
assign value to "{P}:{SIGNAL}{sigCHANNEL}";
monitor value;

// target setpoint parameter.
float setpoint;
assign setpoint to "{P}:{SETPOINT}{setCHANNEL}";
monitor setpoint;

// signal to send callback that the window have been met 
short CB = 0;
assign CB to "{P}:CB{CHANNEL}";


//Variable for the size of the temperature CBthres.
float CBthres = 3.0;
assign CBthres to "{P}:CBthres{CHANNEL}";
monitor CBthres;

//Defining the time window, time for values to be within n spec range, for the callback 
float CBsettl_t = 10.0;
assign CBsettl_t to "{P}:CBsettl_t{CHANNEL}";
monitor CBsettl_t;

//Defining the MAXIMUM time window for the callback, if equ not met within this a CBerr is set 
float CBtout = 20.0;
assign CBtout to "{P}:CBtout{CHANNEL}";
monitor CBtout;


// The state machine puls
float   CBclk;
assign  CBclk to "{P}:CBclk{CHANNEL}";
monitor CBclk;

//Signal for informing about the current state
string	CurrentState;
assign  CurrentState to "{P}:CBstate{CHANNEL}";

// signal to send timeout 
int CBerr;
assign CBerr to "{P}:CBerr{CHANNEL}";

//2 below CAN be changed to local varaibles!!
int CBtot_t = 0;
assign CBtot_t to "{P}:CBtot_t{CHANNEL}";
monitor CBtot_t;

int CBtsettl = 0;
assign CBtsettl to "{P}:CBtsettl{CHANNEL}";
monitor CBtsettl;

//********* declare internal variables ****************

int time0 = 0;
int timeCnt = 0;
int timeSet0 = 0;



//****************************************************************************
ss equilibrium_callback {

  //*********************************************************
  //Startingpoint. Callback inactive in this state.
  // currently NOT used in GUI now. entry is made and then it  continues
  state inactivated {
    entry{
      //printf("i..//./././........IN TGE START!!//////////////");
      strcpy(CurrentState,"inactivated");
      pvPut(CurrentState);

      //Putting out some parameters to initialise records to default values
      // , need to think how to do this...
      CBthres = 3.0;
      pvPut(CBthres);
      CBsettl_t = 10.0;
      pvPut(CBsettl_t);
      CBtout = 20.0;
      pvPut(CBtout);
      CB = 0;
      pvPut(CB);
      CBtsettl = 0;
      pvPut(CBtsettl);
      CBerr = 0;
      pvPut(CBerr);
      CBclk = 0;
      pvPut(CBclk);
      CBtot_t = 0;
      pvPut(CBtot_t);

    }

    when (TRUE) {
    } state moving
  }

  //*********************************************************
  //Starting state to reset timers as Time and Temp
  //states are separated.
  state moving {
    entry{
      strcpy(CurrentState,"moving");
      pvPut(CurrentState);
      pvGet(CBclk);
      timeCnt = CBclk;
      time0 = CBclk;
      CBtot_t = 0;
    } 
    
    when (TRUE){
      //printf("....TRUE next moving temp  !!");
    } state movingTemp
  }

  //*********************************************************
  state movingTemp {

    entry{
      strcpy(CurrentState,"movingTemp");
      pvPut(CurrentState);
      //printf("in moving temp SNL {CHANNEL}  %d", 99);
    }

    when ((value <= (setpoint + CBthres)) && (value >= (setpoint - CBthres))  ){
      //printf("....TRUE next moving TIME");
      //printf("timeTot   %d\n", CBtot_t);
      //printf("in moving temp SNL   %f\n", (setpoint + CBthres));
      //printf("in moving temp SNL   %f\n", (setpoint - CBthres));
    } state movingTime

    when ( (CBtot_t >  CBtout) && (CBerr == FALSE) ) {

    } state timeout


    when (CBclk > timeCnt)  {
      timeCnt = timeCnt + 1 ;  
      CBtot_t = CBclk - time0;
      pvPut(CBtot_t);
      //printf("timeTot   %d\n", CBtot_t);
      //printf("in moving temp SNL   %f\n", (setpoint + CBthres));
      //printf("in moving temp SNL   %f\n", (setpoint - CBthres));
    } state movingTemp

  }

  //*********************************************************
  state movingTime {

    entry{
      strcpy(CurrentState,"MovingTime");
      pvPut(CurrentState); 
      pvGet(CBclk);
      CBtsettl = 0;
      timeSet0  = CBclk;
    }

    when ((value <= (setpoint + CBthres)) && (value >= (setpoint - CBthres)) && (CBtsettl >  CBsettl_t) ){
      //printf("timeTot   %d\n", CBtot_t);
      //printf("in moving temp SNL   %f\n", (setpoint + CBthres));
      //printf("in moving temp SNL   %f\n", (setpoint - CBthres));
    } state onTarget

    // This is added to get the State to evaluate!! As no signal updates!!PROBLEM!!
    when (CBclk > timeCnt)  {
      timeCnt = timeCnt + 1 ;
      CBtot_t = CBclk - time0;
      pvPut(CBtot_t);
      CBtsettl = CBclk - timeSet0;
      pvPut(CBtsettl);
      //printf("timeTot   %d\n", CBtot_t);
      //printf("in moving temp SNL   %f\n", (setpoint + CBthres));
      //printf("in moving temp SNL   %f\n", (setpoint - CBthres));

    } state movingTime

    when ( (CBtot_t >  CBtout) && (CBerr == FALSE) ) {

    } state timeout

    when (     (  value > (setpoint + CBthres)   )   ||  (  value <  (  setpoint - CBthres)   )  ){

    } state movingTemp
  }

  //*********************************************************
  state onTarget {
    entry{
      CB = TRUE;
      pvPut(CB);
      CBerr = FALSE;
      pvPut(CBerr);
      strcpy(CurrentState,"Ready");
      pvPut(CurrentState);

    }

    when ((value > (setpoint + CBthres)) || (value < (setpoint - CBthres)) ) {
      CB = FALSE;
      pvPut(CB);
      //Parameter outside CBthres, restart the process
    } state moving
  }

  //*********************************************************
  state timeout {
    entry{
      strcpy(CurrentState,"timeout");
      pvPut(CurrentState);
      CBerr = TRUE;
      pvPut(CBerr);
    }
    when (TRUE){
      //Flag fault (err), then continue to wait for temp to settle.    
    } state movingTemp
  }
}













