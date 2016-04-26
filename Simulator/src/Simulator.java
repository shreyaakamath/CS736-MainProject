import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

enum Strategy{
  CPU,
  UPFRONT,
  UPFRONT_OPREP,
  CPU_OPREP,
  MAX_CPU,
  MAX_STRATS
}

enum enumClass{
	basic,
	permium,
	enterprise
}


public class Simulator implements Runnable {
	Thread t ;
  	RunParams simulatorRunParameters;
  	HashMap<String,List<CloudDistribution>> instanceMap;
  	List<Instance> allInstances;
  	List<Instance> naiveInstances;
  	HashMap<String,List<Integer>> custBasedOnClass;
  	Customer c;
  	static long maxRand = 4294967295l;
  	String strat;
  	String family;
  	int id;
  
  Simulator(HashMap<String,List<CloudDistribution>> instanceMap,RunParams simulatorRunParameters,String strat,Customer c,HashMap<String,List<Integer>> custBasedOnClass){
	  this.instanceMap=instanceMap;
	  this.simulatorRunParameters=simulatorRunParameters;
	  allInstances=new ArrayList<Instance>();
	  naiveInstances=new ArrayList<Instance>();
	  this.strat=strat;
	  this.family=c.predictedFamily;
	  this.id=c.id;
	  this.custBasedOnClass=custBasedOnClass;
	  this.c=c;
  }
public void start(){
	if (t == null)
    {
       t = new Thread (this, family);
       t.start ();
    }
}
 
 
  
 public void run(){
	  
	  int time = 0; 
	  int num_instances = 0;
	  float total_work = 0;
	  float aggregate_perf = 0;
	  float naive_total_work = 0;
	  float naive_aggregate_perf = 0;
	  double cur_perf = 0;
	  float first_avg = 0;
	  float running_agg_avg = 0;
	  float cur_agg_perf = 0;
	  float delta = 0;
	  int num_migrated = 0;
	  int A=simulatorRunParameters.A;
	  int B=simulatorRunParameters.B;
	  int T =simulatorRunParameters.time;
	  int mu = simulatorRunParameters.expectedNoOfReMig;
	  int m = simulatorRunParameters.migrationPenality;
	  int alphaAgg=simulatorRunParameters.alphaAgg;
	  int alphaServ=simulatorRunParameters.alphaServ;
	  
	  //launch A+B instances 
	  for(int i=0;i<A+B;i++){
		  launch_instance(family, i, 0, time);
		  num_instances++;
	  }
	  
	  Strategy s= Strategy.valueOf(strat);
	  switch(s){
	  	case CPU_OPREP:
	  		running_agg_avg=0;
	  		for(CloudDistribution cd : instanceMap.get(family)){
	  			running_agg_avg+=cd.mean;
	  		}
	  		running_agg_avg=running_agg_avg/instanceMap.get(family).size();
	  		break;
	  	case UPFRONT_OPREP:
	  		running_agg_avg=calc_curr_agg_perf(0,A+B);
	  		break;
	  }
	  first_avg=running_agg_avg;
	  
	  //copy A units to naive stratergy
	  naiveInstances= new ArrayList<Instance>(allInstances);
	  int units=simulatorRunParameters.quantum;
	  time+=units;
	  
	  //end up-front exploration
	  if(T>0 && B>0){
		  if(Strategy.CPU.equals(s)|| Strategy.MAX_CPU.equals(s))
			  Collections.sort(allInstances,new InstanceComparatorType());
		  else if (Strategy.UPFRONT.equals(s)||Strategy.UPFRONT_OPREP.equals(s))
			  Collections.sort(allInstances,new InstanceComparatorPerf());
		  
		 //kill B bad instances based on above stratergies
		  for(int i=A;i<A+B;i++)
			  calcPerfStateAndKill(allInstances.get(i), time);
	  }
	  
	  //work with best A as of now and do opportunistic replacements
	  if(Strategy.CPU_OPREP.equals(s)|| Strategy.UPFRONT_OPREP.equals(s)|| Strategy.MAX_CPU.equals(s)){
		  for(int i=1;i<T-1;i++){
			  System.out.println("Time = "+time/units);
			  delta=mu*(m/units)/(T-i);
			  num_migrated=0;
			  for(int j=0;j<allInstances.size();j++){
				  Instance inst=allInstances.get(j);
				  //get the mean from corresponding family/processor type
				  double mean=0;
				  for(CloudDistribution cd : instanceMap.get(inst.family)){
					  if(cd.processor.equalsIgnoreCase(inst.proccessor)){
						  mean=cd.mean;
					  }
				  }
				  
				  if(inst.active==1){
					  if(Strategy.CPU_OPREP.equals(s)|| Strategy.UPFRONT_OPREP.equals(s)){
						  switch(s){
						  case CPU_OPREP:
							  cur_perf=mean;
							  break;
						  case UPFRONT_OPREP:
							  //can add optimization to prevent many migrations
							  //if(simulatorRunParameters.alphaAgg!=0)
							  cur_agg_perf = calc_curr_agg_perf(i, allInstances.size());
							  running_agg_avg=alphaAgg*cur_agg_perf+(1-alphaAgg)*running_agg_avg;
							  if(j>1)
							  inst.curPerf=alphaServ * inst.perf[i]+(1-alphaServ)*allInstances.get(j-1).curPerf;
							  cur_perf=inst.curPerf;
							  break;
						default:
							System.out.println("error unknown strategy ");
							break;
						  }
						  
						 if(running_agg_avg - cur_perf > delta){
							 // TODO based on VM perf , cost , perf threshold decide whether to move to other family or other processor
							 System.out.println("Migrating type "+ family +" because "+running_agg_avg +" > "+ cur_perf);
							 launch_instance(family, num_instances+num_migrated, i, time);
							 num_migrated++;
							 calcPerfStateAndKill(inst, time);
						 }
					  }
					  else if(Strategy.MAX_CPU.equals(s)){
						  if(inst.family!=null){
							  System.out.println("Migrating type "+ family);
							  launch_instance(family, num_instances+num_migrated, i, time);
							  num_migrated++;
						      calcPerfStateAndKill(inst, time);
						  }
					  }
				  }
			  }
			  num_instances+=num_migrated;
			  time+=units;
		  }
		  time+=units;
	  }else{
		  time+=units*(T-1);
	  }
	  
	  if(time!=T*units){
		  System.out.println("Error in simualtor code time!=T*units . Exiting");
		  System.exit(0);
	  }
	  
	  //Loop through all of num_instances
	  for(Instance inst : allInstances){
		  
		  if(inst.active==1){
			  collaborate(inst,time);
		  }
		  System.out.println("inst total work "+ inst.totalWork);
		  total_work+=inst.totalWork;
	  }
	 
	  System.out.println("done with current strategy, killing naive instances");
	  time=units*T;
	  for(int i=0;i<A;i++){
		  calcPerfStateAndKill(naiveInstances.get(i), time);
		  naive_total_work+=naiveInstances.get(i).totalWork;
	  }
	  
	  aggregate_perf=total_work/(float)((A*T+B)*units);
	  naive_aggregate_perf=naive_total_work/(A*T*units);
	  System.out.println("Printing for customer ------------"+id);
	  System.out.println(s.name()+" "+T+" "+units+" "+A+" "+B+" "+m+" "+mu+" "+alphaAgg+" "+alphaServ);
	  System.out.println("Naive perfs:"+ naive_total_work);  //their code has printed total_work ??
	  for(Instance inst: naiveInstances) System.out.println(inst.family+" "+inst.id+" "+ inst.avgPerf+" total work -"+inst.totalWork+" total time "+inst.totalTime);
	  System.out.println("Number of instances "+ num_instances);
	  System.out.println("Number migrated "+ (num_instances-A-B));
	  System.out.println("First round average+ "+first_avg);
	  System.out.println("Total work "+ total_work);
	  System.out.println("Effective rate "+ aggregate_perf);
	  System.out.println("Naive total work "+ naive_total_work);
	  System.out.println("Naive effective rate"+naive_aggregate_perf);
	  System.out.println("Speedup "+(double)aggregate_perf/(double)naive_aggregate_perf);
	  System.out.println("Percentage improvement "+(double)(aggregate_perf/(double)naive_aggregate_perf-1)*100);
  }

 void collaborate(Instance instToKill,int time){
	 calcPerfStateAndKill(instToKill, time);
	 float threashold = 5;
	 if(instToKill.curPerf > threashold){
		//this instance has good performance , lets give to a customer of the same class
		List<Integer> custSameClass = custBasedOnClass.get(c.custClass);
		for(Instance inst : allInstances){
			//dont swap with same instance
			if(inst.id== instToKill.id) continue;
			if(inst.active ==1){
				//if instance is active and belongs to cust from same class
				if (custSameClass.contains(inst.customerId)){
					threashold=20;
					if(inst.curPerf < threashold){
						System.out.println("==================swapping =========================");
						//and this instance has below threshold performance so can swap
						swapInstance(instToKill,inst);
						break;
					}
				}
			}
		}
	 }else{
		 //since this instances perf if below threshold we will not swap it with anything else
		 calcPerfStateAndKill(instToKill, time);
	 }
 }
 
 void swapInstance(Instance original , Instance next){
	 next.proccessor=original.proccessor;
 }
   long get_rand(){
	  long result = 0;
	  try {
		FileInputStream randomFile = new FileInputStream("/dev/urandom");
		byte[] data = new byte[4]; 
		try {
			randomFile.read(data);
		} catch (IOException e) {
			e.printStackTrace();
		}
		if(data !=  null)
		{
			result = ByteBuffer.wrap(data).getInt();
		}
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	}
	  return result; 
  }
  /**
   * 
   * @return
   */
  float gen_std_normal(){
	  float u1,u2,x,r;
	  double PI=3.14159265358979323846d;
	  //Random rand=new Random();
	  long n1 = get_rand(); 
	  long n2 = get_rand();
/*	  while(true){
		  n1 = get_rand();
		  if(n1 < 0) break;
		  else continue;
	  }*/
	  u1=n1/(float)maxRand;
//	  System.out.println("U1 random = " + n1);
	/*  while(true){
		  n2 = get_rand();
		  if(n2 < 0) break;
		  else continue;
	  }*/
	  u2=n2/(float)maxRand;
//	  System.out.println("U2 random = " + n2);
	  //u1=rand.nextInt()/(float)maxRand;
	  //u2=rand.nextInt()/(float)maxRand;
	  
	  float log=(float)Math.log(u1);
	  x=(float)Math.sqrt(-2*log)*(float)Math.cos(2*PI*u2);
	  return x;
  }
 
  /**
   * 
   * @param t
   * @param numInstances
   * @return
   */
  float calc_curr_agg_perf(int t, int numInstances){
	  int numActive=0;
	  float aggPerf=0;
	  
	  for(Instance inst : allInstances){
		  if(inst.active==1){
			  aggPerf+=inst.perf[t];
			  numActive++;
		  }
	  }
	  
	  return aggPerf/(float)numActive;
  }
  

  void calcPerfStateAndKill(Instance inst, int time){
	    int t,runtime=0;
	    inst.endTime=time;
	    inst.totalTime=inst.endTime-inst.startTime;
	    inst.totalTimeComputation=inst.totalTime-simulatorRunParameters.migrationPenality;
	    inst.active=0;
	    inst.totalWork=0;
	    int units=simulatorRunParameters.quantum;
	    int penalty=simulatorRunParameters.migrationPenality;
	    for(t=inst.startQuantum;runtime<inst.totalTimeComputation;t++){
	    	if(t==0){
	    		inst.totalWork+=(units-penalty)*inst.perf[t];
	    		runtime+=units-penalty;
	    	}else{
	    		inst.totalWork+=units*inst.perf[t];
	    		runtime+=units;
	    	
	    	}
	    }
	    inst.avgPerf=(float)inst.totalWork/(float)inst.totalTime;
	    System.out.println("Killing instance of type "+inst.family+" id="+inst.id);
	  }

  

  
  /**
   * Launch an instance and update all internal data structures
   * @param cdInstance
   * @param id -> unique id for instance 
   * @param t -> current time unit
   * @param time -> not sure ??
   */
  void launch_instance(String family,int id,int t, int time){
	  String whichFamily=family;
	  String whichProcessor=null;
	  double mean=0;
	  double stddev=0;
	  double runFrac;
	  double cumFrac=0;
	  int quantaForSimulation=this.simulatorRunParameters.time;
	
	  //TODO check if no of instances is greater than max possible instances
	  
	  //select the instance of the given type randomly
	  long n3 = get_rand();
//	  System.out.println("runFrac random = " + n3);
	  runFrac=(double)(1-(double)n3)/(double)maxRand;
	  for(CloudDistribution cd:instanceMap.get(whichFamily)){
		  cumFrac+=cd.fraction;
		  if(runFrac<=cumFrac){
			  whichProcessor=cd.processor;
			  mean = cd.mean;
			  stddev=cd.stddev;
			  break;
		  }
	  }
    
	  //add this given instance to the instance variable lists
	  Instance inst= new Instance(id, whichFamily, whichProcessor, 1, time, t,c.id);
	  allInstances.add(inst);
	  
	  //TODO bimodal frac 
	  
	  //set performance parameters
	  for(int i=0;i<quantaForSimulation;i++){
		  inst.perf[i]=stddev*gen_std_normal()+mean;
	  }
	  inst.curPerf=inst.perf[t];
	  System.out.println("Launching instance of family "+whichFamily+", processor"+whichProcessor+" id "+id+"Performance of launched instance "+inst.curPerf);
  }
  
  
  public static void main(String args[]){
	  PredictFamily MLObj = new PredictFamily("custInfo.csv", "custInfoAfterPrediction.csv");
	  HashMap<String,List<CloudDistribution>> instanceMap=Helper.getDistribution("ner1-config");
	  List<Customer> customerInfoList=Helper.getCustomerInfo(MLObj.getOutputFilename());
	  //List<Customer> customerInfoList=Helper.getCustomerInfo("custInfoAfterPrediction.csv");
	  //List<Customer> customerInfoList=Helper.getCustomerInfo("custInfo.csv");
	  RunParams simulatorRunParameters=Helper.getRunParams("runConfig.prop");
	  HashMap<String,List<Integer>> custBasedOnClass = Helper.getClassifiedCust(customerInfoList);
	  
	  
	  for(Customer c : customerInfoList){
//		  c.predictedFamily="micro";
		  Simulator sim = new Simulator(instanceMap,simulatorRunParameters,Strategy.values()[simulatorRunParameters.strategy].toString(),c,custBasedOnClass);
		  sim.start();
	  }
  }
}

