/*******************************************************************************
  sim-strat.c
  This simulates various cloud gaming strategies. Takes as input the name of 
  a configuration file. 

  Changes:
  - Enabled different distributions of instance types 
  - Added CPU_OPREP strategy
  - Fixed seeming bug in the kill_instance function
  - Disabled doing migration in last time slot

 *******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>






//
// Constants
//

#define WORK_PER_UNIT 20000
#define MAX_INSTANCE_TYPES 100
#define MAX_INSTANCES 1000
#define MAX_TIME_QUANTUMS 1000
#define MAX_LINE 1000
#define START_INSTANCE_EVENT_STR  "launch instance"
#define KILL_INSTANCE_EVENT_STR    "kill instance"
#define MIGRATED_EVENT_STR        "migrate instance"
typedef struct INSTANCETYPE_S {
  float frac; // Fraction of instances of this type
  float mean; // The mean for normal distribution dictating performance
  float stddev; // The standard deviation for normal distribution dictating performance
  float bimodal_frac; // The fraction of time we should be in second mode
  float mean2; // The second mean for bimodal distributions 
  float stddev2; // The second standard deviation for normal distribution dictating performance
} INSTANCETYPE_T, *PINSTANCETYPE_T;

typedef struct INSTANCE_S {
  int id;
  int type;
  int active;
  int start_time;
  int start_quantum;
  int end_time;
  int total_time;                 // Total time running
  float total_time_computation;   // Total time spent doing real work = total_time - migration costs
  float total_work;
  float avg_perf;                 // Used for total performance over course of run
  float cur_perf;                 // Used for moving calculation of performance
  float perf[MAX_TIME_QUANTUMS];  // performance in operations per second
} INSTANCE_T, *PINSTANCE_T;

typedef enum STRAT_S {
  CPU,     // Upfront A+B exploration, pick based on CPU type
  UPFRONT, // Upfront A+B exploration, pick based on first quantum perf
  UPFRONT_OPREP, // Upfront A+B exploration, pick based on first quantum perf,
                 // and do opportunistic replacement based on first quantum average
  CPU_OPREP, // Upfront A+B exploration, pick based on CPU type and do 
             // opportunistic replacement using predefined CPU averages 
             // to determine current instance's perf and average perf
  MAX_CPU,
  MAX_STRATS
} STRAT_T;

INSTANCETYPE_T instanceTypes[MAX_INSTANCE_TYPES];
INSTANCE_T instances[MAX_INSTANCES];
INSTANCE_T naive_instances[MAX_INSTANCES];
unsigned int num_instance_types = 0;
char active_nodes[MAX_INSTANCES];
STRAT_T strat;     // max number time quantums
unsigned int T;     // max number time quantums
unsigned int units; // size of quantum in seconds
unsigned int A;     // number of instances to keep running in quantums > 1
unsigned int B;     // number of exploratory instances to run in quantum 1
unsigned int m;     // migration penalty in seconds
float mu;           // expected number of remigrations (we can calculate this as well)
float alphaAgg;     // EWMA threshold for aggregate performance
float alphaServ;    // EWMA threshold for individual instance performance

//float opt_perf = 0;


//TODO: right now hardcoded to look at first quantum's perf
int compare_instance_by_perf(const void * arg1, const void * arg2) {
  PINSTANCE_T p1 = (PINSTANCE_T) arg1;
  PINSTANCE_T p2 = (PINSTANCE_T) arg2;
  if (p1->perf[0] < p2->perf[0]) {
    return(1);
  } else if (p1->perf[0] > p2->perf[0]) {
    return(-1);
  } else {
    return(0);
  }
}

int compare_instance_by_type(const void * arg1, const void * arg2) {
  PINSTANCE_T p1 = (PINSTANCE_T) arg1;
  PINSTANCE_T p2 = (PINSTANCE_T) arg2;
  if (p1->type > p2->type) {
    return(1);
  } else if (p1->type < p2->type) {
    return(-1);
  } else {
    return(0);
  }
}



//
// Get random 32-bit number
// 
FILE *uRand = NULL;
#define MY_RAND_MAX 4294967295 // 2^32 - 1
unsigned int get_rand(void) 
{
  FILE *uRand;
  unsigned int ret;
  int numread = 102;

  // A good source of randomness in unix systems.
  uRand = fopen("/dev/urandom", "r");
  
  if(!uRand) {
    printf("Error opening /dev/urandom , returning random value from stack");
    return ret; //some random value in the stack
  }
  //numread = read( uRand, &ret, 4 );
  if( fread( &ret, sizeof(unsigned char), 4, uRand ) <= 0 ) {
    printf( "Error reading from /dev/urandom" ); 
  }

  fclose( uRand );
  return ret;
}


#define PI 3.14159265358979323846
float gen_std_normal()
{
  float u1,u2,x;
  float r;

  u1 = get_rand() / (float)MY_RAND_MAX;
  u2 = get_rand() / (float)MY_RAND_MAX;

  x = sqrt(-2 * log(u1)) * cos(2 * PI *u2);
  return(x);
}

// 
// Log events
//
void log_event(int instance, int time_sec, char * event)
{
  printf("%10d %5d %s\n",time_sec, instance, event);
}

//
// Calculate the average over last steps for active nodes
//
/*
float active_average(void)
{
  static int calls = 0;
  float sum = 0;
  float cnt = 0;
  int  i;
  calls++;
  if (calls < 100) {
    return(-1);
  }

  for (i = 0; i < num_instances;i++) {
    if (active_nodes[i] && (instances[i].average != 0.0)) {
      sum += instances[i].average;
      cnt += 1.0;
    }
  }
  return(sum/cnt);
  
}
*/


void launch_instance( PINSTANCE_T inst, int id, int t, int time )
{
  static int total_num_instances = 0;
  int i = 0;
  // TODO: Pick the instance type according to frac's. For now, just uniformly
  int whichType;
  int ranPhaseChange;
  double ranFrac;
  double cumFrac = 0;

  total_num_instances++;
  if( total_num_instances == MAX_INSTANCES ) { 
    printf("Error: ran out of space of instances\n" );
    exit(-1);
  }
  
  
  // This chooses the instance type uniformly as weighted by type fractions
  ranFrac =  (double) (1 - (double)get_rand() / (double)MY_RAND_MAX); 
  for( i = 0; i < num_instance_types; i++ ) {
    cumFrac += instanceTypes[i].frac;
    if( ranFrac <= cumFrac ) {
      whichType = i;
      break;
    }
  }

  inst->id = id; 
  inst->type = whichType; 
  inst->start_time = time; 
  inst->start_quantum = t; 
  inst->active = 1;

  // Treat phase changes as uniformly distributed in time
  // We also ignore bimodal_frac for now
  if( instanceTypes[i].bimodal_frac > 0 ) {
    ranPhaseChange =  get_rand() % T; 
    printf( "ranPhaseChange: %d\n", ranPhaseChange );
  }
  else {
    ranPhaseChange = T;
  }

  // TODO: probably want to make this same format as traces from real runs?
  printf("LAUNCHING Instance %d, type %d\n", id, whichType );
  // For now just precompute all the per-quantum perfs
  for( i = 0; i < T; i++ ) {
    //inst->perf[i] = (instanceTypes[whichType].stddev * RNOR) + instanceTypes[whichType].mean;
    if( i < ranPhaseChange ) 
      inst->perf[i] = (instanceTypes[whichType].stddev * gen_std_normal() ) + instanceTypes[whichType].mean;
    else
      inst->perf[i] = (instanceTypes[whichType].stddev2 * gen_std_normal() ) + instanceTypes[whichType].mean2;
  }
  inst->cur_perf = inst->perf[t];
  log_event( inst->id, time/units, START_INSTANCE_EVENT_STR );
}

void kill_instance( PINSTANCE_T inst, int time )
{
  int numQuants = 0;
  int t,runtime;

  inst->end_time = time;   
  inst->total_time = inst->end_time - inst->start_time;
  inst->total_time_computation = inst->total_time - m;
  inst->active = 0;
  inst->total_work = 0;
  //for( i = 0; i < numQuants; i++ ) {
  //if start_time is not zero, we are using generated perf[i:0 to T-(end_time-start_time)]
  // FIXED:  t was being compared against hours in the for loop end condition, but was having 
  // in loop seconds added to it
  // CHANGED: I wanted to start using the perf entries associated with the quantums where the
  // instance actually ran. This is  because now we're computing aggregate performance and need
  // to be globally consistent about which entries in perf we use for which time quantums.
  for( t = inst->start_quantum, runtime = 0; runtime < inst->total_time_computation; t++ ) {
    if( t == 0 ) {
      inst->total_work += (units-m) * inst->perf[t]; // subtract migration cost from first running quantum
      runtime += units - m;
    }
    else {
      inst->total_work += units * inst->perf[t];
      runtime += units;
    }
  }
  inst->avg_perf = inst->total_work / inst->total_time;
  printf( "KILLING %d of type %d at %d\n", inst->id, inst->type, time/units );
  //log_event( inst->id, time, KILL_INSTANCE_EVENT_STR );
}

/*
void calculate_optimal() {
  int i;
  float tmp;
  for(i = 0; i < num_instance_types; i++) {
    tmp = instanceTypes[i].mean + instanceTypes[i].stddev;
    if( tmp > opt_perf )
      opt_perf = tmp;
  }

}
*/


float calc_curr_agg_perf( int t, int num_instances )
{
  int i;
  int num_active = 0;
  float agg_perf = 0;

  for( i = 0; i < num_instances; i++ ) {
    if( instances[i].active ) {
      agg_perf += instances[i].perf[t];
      num_active++;
    }
  }

  return agg_perf / (float)num_active;
}


//
// Run the A+B simulation
//
void simulate(void)
{
  int time = 0; 
  int whichType = 0;
  int i = 0;
  int j = 0;
  int num_instances = 0;
  float total_work = 0;
  float aggregate_perf = 0;
  float naive_total_work = 0;
  float naive_aggregate_perf = 0;
  float cur_perf = 0;
  int num_active = 0;
  float first_avg = 0;
  float running_agg_avg = 0;
  //float agg_avg = 0;
  float cur_agg_perf = 0;
  float stddev = 0;
  float delta = 0;
  int num_migrated = 0;

  //calculate_optimal();

  // Start with launching A+B instances
  for( i = 0; i < A+B; i++ ) {
    launch_instance( &instances[i], i, 0, time );
    num_instances++;
    //stddev += instances[i].perf[0] * instances[i].perf[0];
  } 
  
  switch( strat ) {
    case CPU_OPREP:
      running_agg_avg = 0;
      for( i = 0; i < num_instance_types; i++ ) {
        running_agg_avg += instanceTypes[i].mean;
      }
      running_agg_avg = running_agg_avg / num_instance_types;
      break;
    case UPFRONT_OPREP:
      running_agg_avg = calc_curr_agg_perf( 0, A+B ); 
      //stddev = sqrt( stddev / (float)(A+B)  - agg_avg*agg_avg ); 
      break;
  }

  first_avg = running_agg_avg;

  // Copy over first A units for Naive strategy
  memcpy( naive_instances, instances, A*sizeof(INSTANCE_T) );
  time += units; 

  // Up-front exploration ends
  if( T > 0 && B > 0 ) {
    if( strat == CPU || strat == MAX_CPU ) 
      qsort( instances, A+B, sizeof(INSTANCE_T), compare_instance_by_type);
    else if( strat == UPFRONT || strat == UPFRONT_OPREP ) 
      qsort( instances, A+B, sizeof(INSTANCE_T), compare_instance_by_perf);

    //Kill B bad instances for all strategies
    for( i = A; i < A+B; i++ )  kill_instance( &instances[i], time );
  }


  //Working with best A as of now, and do opportunistic replacements for *seemingly* bad ones
  if( strat == CPU_OPREP || strat == UPFRONT_OPREP || strat == MAX_CPU  ) {
    // Quantums 2 and on perform opportunistic replacement
    for( i = 1; i < T-1; i++ ) {
      printf("TIME: %d\n", time/units);
      delta = mu * (m/(float)units) / (T - i);
      num_migrated = 0;
      for( j = 0; j < num_instances; j++ ) {
        if( instances[j].active ) {
          if( strat == CPU_OPREP || strat == UPFRONT_OPREP ) { 
            switch( strat ) {
              case CPU_OPREP:
                cur_perf = instanceTypes[instances[j].type].mean;
                break;
              case UPFRONT_OPREP:
		if( alphaAgg != 0 ) //Optimization to avoid this costly step when it is unnecessary
		  cur_agg_perf = calc_curr_agg_perf( i, num_instances );
                running_agg_avg = alphaAgg * cur_agg_perf + (1 - alphaAgg) * running_agg_avg;

                instances[j].cur_perf = alphaServ * instances[j].perf[i] + (1 - alphaServ) * instances[j-1].cur_perf; 
                cur_perf = instances[j].cur_perf;
                break;
              default:
                printf( "Error: unknown strategy type %d at line %d", strat, __LINE__ );
                break;
            }

            if( running_agg_avg - cur_perf > delta ) {
              printf("MIGRATING type %d because (%f - %f) = %f  > %f  \n", instances[j].type, running_agg_avg, cur_perf, running_agg_avg - cur_perf, delta);
              log_event( instances[j].id, time/units, MIGRATED_EVENT_STR );

              launch_instance( &instances[num_instances + num_migrated], num_instances + num_migrated, i, time );
              num_migrated++;
              kill_instance( &instances[j], time );
            }
          }
          else if( strat == MAX_CPU ) {
            if( instances[j].type > 0 ) {
              printf("MIGRATING type %d\n", instances[j].type );
              log_event( instances[j].id, time/units, MIGRATED_EVENT_STR );

              launch_instance( &instances[num_instances + num_migrated], num_instances + num_migrated, i, time );
              num_migrated++;
              kill_instance( &instances[j], time );
            }
          }
        } 
      }
      num_instances += num_migrated;
      time += units;
    }
    time += units;
  }
  else {
    time += units*(T-1);
  }

  assert(time == T*units);

  //Loop through all of num_instances 
  for( i = 0; i < num_instances; i++ ) {
    if( instances[i].active ) {
      kill_instance( &instances[i], time );
    }
    total_work += instances[i].total_work;
  }

  printf("Done with current strategy, killing naive instances... \n");
  // Calculate total work done and total rate for naive
  time = units*T;
  for( i = 0; i < A; i++ ) {
    kill_instance( &naive_instances[i], time );
    naive_total_work += naive_instances[i].total_work;
  }

  aggregate_perf = total_work / (float) ((A*T+B) * units);
  naive_aggregate_perf = naive_total_work / (float) ((A*T) * units);

  printf( "%d,%d,%d,%d,%d,%d,%f,%f,%f \n ", strat, T, units, A, B, m, mu, alphaAgg, alphaServ );
  
  printf( "Up-front selected perf: ", total_work );
  for( i = 0; i < A; i++ ) { 
    printf( "(%d,%d,%.2f) ", instances[i].type, instances[i].id,  instances[i].avg_perf );
  }
  printf( "\nNaive perfs           : ", total_work );
  for( i = 0; i < A; i++ ) { 
    printf( "(%d,%d,%.2f) ",  naive_instances[i].type, naive_instances[i].id, naive_instances[i].avg_perf );
  }
  printf( "\n\nNumber of instances: %d\n", num_instances);
  printf( "Number Migrated: %d\n", num_instances - A - B);
  printf( "First round average: %f\n", first_avg );

  printf( "Total work: %f\n", total_work );
  printf( "Effective rate:  %f\n", aggregate_perf );
  printf( "Naive total work: %f\n", naive_total_work );
  printf( "Naive effective rate:  %f\n", naive_aggregate_perf );
  // printf( "Optimal performance: %f\n", opt_perf );
  printf( "Speedup:  %f\n", aggregate_perf / naive_aggregate_perf );
  printf( "Percentage-Improvement:  %f\n", ((aggregate_perf / naive_aggregate_perf)-1)*100 );
  //printf( "Perc-diff-with-optimal:  %f\n", ((opt_perf/naive_aggregate_perf)-1)*100 );  
}

int main(int argc, char * argv[])
{
  FILE * input = NULL;
  char line[MAX_LINE];
  char * temp;
  int i;
  int err = 0;
  int line_cnt = 0;

  if (argc < 2) {
    printf("Usage: %s config-file\n",argv[0]);
    err = -1;
    goto Cleanup;
  }

  // 
  // Read in instance types from config file
  //
  input = fopen(argv[1],"r");
  if (input == NULL) {
    printf("Error: file %s could not be opened for reading\n",argv[1]);
    err = -1;
    goto Cleanup;
  }


  line_cnt = 0;
  while (fgets(line, MAX_LINE, input) != NULL) {
    //
    // ignore comments
    //
    if( line[0] == '#' ) {
      continue;
    }

    //
    // Parsing: first line is strategy specification: T,A,B,m,mu,alphaAgg,alphaServ
    //
    if(line_cnt == 0) {
      sscanf( line, "%u,%u,%u,%u,%u,%u,%f,%f,%f", &strat, &T, &units, &A, &B, &m, &mu, &alphaAgg, &alphaServ );
      if( (strat < 0) || (strat > MAX_STRATS) || (T > MAX_TIME_QUANTUMS) || (A + B > MAX_INSTANCES) ) {
        printf("Malformed strategy specification: %s:%ld\n", line,strlen(line) );
        err = -1;
        goto Cleanup;
      }
    }
    else {
      // Parsing: instance identifier, frac, mean, stddev 
      //
      temp = strtok(line," \n\t");
      if ((temp == NULL) || (strlen(temp) > 20)) {
        printf("Malformed identifier: %s:%ld\n",line,strlen(line));
        err = -1;
        goto Cleanup;
      }
      // We ignore the instance identifier for now; just use a number instead
      
      temp = strtok(NULL," \n\t");
      if ((temp == NULL) || (strlen(temp) > 20)) {
        printf("Malformed cpuid: %s\n",line);
        err = -1;
        goto Cleanup;
      }
      instanceTypes[num_instance_types].frac = strtof(temp,NULL);

      temp = strtok(NULL," \n\t");
      if ((temp == NULL) || (strlen(temp) > 20)) {
        printf("Malformed command: %s\n",line);
        err = -1;
        goto Cleanup;
      }
      instanceTypes[num_instance_types].mean = strtof(temp,NULL);
   
      temp = strtok(NULL," \n\t");
      if ((temp == NULL) || (strlen(temp) > 20)) {
        printf("Malformed command: %s\n",line);
        err = -1;
        goto Cleanup;
      }
      instanceTypes[num_instance_types].stddev = strtof(temp,NULL); 

      // For bimodal distributions, we may have three more fields: bimodal_frac, mean2, stddev2
      temp = strtok(NULL," \n\t");
      if ((temp != NULL) && (strlen(temp) <= 20)) {
        instanceTypes[num_instance_types].bimodal_frac = strtof(temp,NULL); 
        
        temp = strtok(NULL," \n\t");
        if ((temp == NULL) || (strlen(temp) > 20)) {
          printf("Malformed command: %s\n",line);
          err = -1;
          goto Cleanup;
        }
        instanceTypes[num_instance_types].mean2 = strtof(temp,NULL); 

        temp = strtok(NULL," \n\t");
        if ((temp == NULL) || (strlen(temp) > 20)) {
          printf("Malformed command: %s\n",line);
          err = -1;
          goto Cleanup;
        }
        instanceTypes[num_instance_types].stddev2 = strtof(temp,NULL); 
      }

      num_instance_types++;
    }
    line_cnt++;
  }


  // 
  // Seed the randomness needed for simulation
  // 
  //zigset( get_rand() );
  
  //
  // Prepare rng access
  //
  uRand = fopen("/dev/urandom", "r");
  if(!uRand) {
    printf("Error opening /dev/urandom\n" );
    goto Cleanup; //some random value in the stack
  }


  //
  // Perform simulation
  //
  switch( strat ) {
    case CPU:
    case UPFRONT:
    case UPFRONT_OPREP:
    case CPU_OPREP:
    case MAX_CPU:
      simulate();
      break;
    default:
      printf( "Error: unrecognized strategy %d\n", strat );
  }
 
 
 
 Cleanup:
  if (input != NULL)
    fclose(input);
  if (uRand != NULL)
    fclose(uRand);
  return(0);
}



////////////////////////////////////////////////////////////////////////////////
// JUNKYARD
////////////////////////////////////////////////////////////////////////////////

#if(0)

/*
 * TomR: The code below is form http://www.jstatsoft.org/v05/i08/supp/1
 * It appears to be a canonical way to sample from a normal distribution.
 */

/* The ziggurat method for RNOR and REXP
Combine the code below with the main program in which you want
normal or exponential variates.   Then use of RNOR in any expression
will provide a standard normal variate with mean zero, variance 1,
while use of REXP in any expression will provide an exponential variate
with density exp(-x),x>0.
Before using RNOR or REXP in your main, insert a command such as
zigset(86947731 );
with your own choice of seed value>0, rather than 86947731.
(If you do not invoke zigset(...) you will get all zeros for RNOR and REXP.)
For details of the method, see Marsaglia and Tsang, "The ziggurat method
for generating random variables", Journ. Statistical Software.
*/

static unsigned long jz,jsr=123456789;

#define SHR3 (jz=jsr, jsr^=(jsr<<13), jsr^=(jsr>>17), jsr^=(jsr<<5),jz+jsr)
#define UNI (.5 + (signed) SHR3*.2328306e-9)
#define IUNI SHR3

static long hz;
static unsigned long iz, kn[128], ke[256];
static float wn[128],fn[128], we[256],fe[256];

#define RNOR (hz=SHR3, iz=hz&127, (fabs(hz)<kn[iz])? hz*wn[iz] : nfix())
#define REXP (jz=SHR3, iz=jz&255, (    jz <ke[iz])? jz*we[iz] : efix())

/* nfix() generates variates from the residue when rejection in RNOR occurs. */

float nfix(void)
{
const float r = 3.442620f;     /* The start of the right tail */
static float x, y;
 for(;;)
  {  x=hz*wn[iz];      /* iz==0, handles the base strip */
     if(iz==0)
       { do{ x=-log(UNI)*0.2904764; y=-log(UNI);}	/* .2904764 is 1/r */
        while(y+y<x*x);
        return (hz>0)? r+x : -r-x;
       }
                         /* iz>0, handle the wedges of other strips */
      if( fn[iz]+UNI*(fn[iz-1]-fn[iz]) < exp(-.5*x*x) ) return x;

     /* initiate, try to exit for(;;) for loop*/
      hz=SHR3;
      iz=hz&127;
      if(fabs(hz)<kn[iz]) return (hz*wn[iz]);
  }

}

/* efix() generates variates from the residue when rejection in REXP occurs. */
float efix(void)
{ float x;
 for(;;)
  {  if(iz==0) return (7.69711-log(UNI));          /* iz==0 */
     x=jz*we[iz]; if( fe[iz]+UNI*(fe[iz-1]-fe[iz]) < exp(-x) ) return (x);

      /* initiate, try to exit for(;;) loop */
   jz=SHR3;
   iz=(jz&255);
   if(jz<ke[iz]) return (jz*we[iz]);
  }
}
/*--------This procedure sets the seed and creates the tables------*/

void zigset(unsigned long jsrseed)
{  const double m1 = 2147483648.0, m2 = 4294967296.;
   double dn=3.442619855899,tn=dn,vn=9.91256303526217e-3, q;
   double de=7.697117470131487, te=de, ve=3.949659822581572e-3;
   int i;
   jsr^=jsrseed;

/* Set up tables for RNOR */
   q=vn/exp(-.5*dn*dn);
   kn[0]=(dn/q)*m1;
   kn[1]=0;

   wn[0]=q/m1;
   wn[127]=dn/m1;

   fn[0]=1.;
   fn[127]=exp(-.5*dn*dn);

    for(i=126;i>=1;i--)
    {dn=sqrt(-2.*log(vn/dn+exp(-.5*dn*dn)));
     kn[i+1]=(dn/tn)*m1;
     tn=dn;
     fn[i]=exp(-.5*dn*dn);
     wn[i]=dn/m1;
    }

/* Set up tables for REXP */
    q = ve/exp(-de);
    ke[0]=(de/q)*m2;
    ke[1]=0;

    we[0]=q/m2;
    we[255]=de/m2;

    fe[0]=1.;
    fe[255]=exp(-de);

   for(i=254;i>=1;i--)
  {de=-log(ve/de+exp(-de));
   ke[i+1]= (de/te)*m2;
   te=de;
   fe[i]=exp(-de);
   we[i]=de/m2;
  }
}

#endif







