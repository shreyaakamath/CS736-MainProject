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

enum Family{
	nano,
	micro,
	small
}

public class Simulator {
	
	HashMap<String,Integer> familyMap;
	HashMap<Integer,String> revFamilyMap;
  	RunParams simulatorRunParameters;
  	HashMap<String,List<CloudDistribution>> instanceMap;
  	List<Instance> allInstances;
  	List<Instance> naiveInstances;
  	HashMap<String,List<Integer>> custBasedOnClass;
  	Customer currentCust;
  	static long maxRand = 4294967295l;
  	String stratStr;
  	String family;
  	Strategy currStratObj;
  	int num_instances;
  	int time;
  	float first_avg;
  	int num_migrated;
  	HashMap<String,Collaborator> collaboratorMap;
  
  Simulator(HashMap<String,List<CloudDistribution>> instanceMap,RunParams simulatorRunParameters,String strat,Customer c,HashMap<String,List<Integer>> custBasedOnClass,HashMap<String,Collaborator> collaboratorMap){
	  this.instanceMap=instanceMap;
	  this.simulatorRunParameters=simulatorRunParameters;
	  allInstances=new ArrayList<Instance>();
	  naiveInstances=new ArrayList<Instance>();
	  this.stratStr=strat;
	  this.family=c.predictedFamily;
	  this.custBasedOnClass=custBasedOnClass;
	  this.currentCust=c;
	  this.collaboratorMap=collaboratorMap;
	  currStratObj= Strategy.valueOf(strat);
	  num_instances =0;
	  time=0;
	  first_avg = 0;
	  num_migrated=0;
	  familyMap = new HashMap<String,Integer>();
	  revFamilyMap = new HashMap<Integer,String>();
	  
	  int i=0;
	  for(Family f : Family.values()){
		  familyMap.put(f.toString(),i);
		  revFamilyMap.put(i,f.toString());
		  i++;
	  }
  }
 

  public void simulateZero(){
	  
	  float running_agg_avg = 0;
	  int A=simulatorRunParameters.A;
	  int B=simulatorRunParameters.B;
	  int T =simulatorRunParameters.time;
	  int units=simulatorRunParameters.quantum;
	  
	  //launch A+B instances 
	  for(int i=0;i<A+B;i++){
		  launch_instance(i, 0, time);
		  num_instances++;
	  }
	  
	  
	  switch(currStratObj){
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
	  
	  time+=units;
	  
	  //end up-front exploration
	  if(T>0 && B>0){
		  if(Strategy.CPU.equals(currStratObj)|| Strategy.MAX_CPU.equals(currStratObj))
			  Collections.sort(allInstances,new InstanceComparatorType());
		  else if (Strategy.UPFRONT.equals(currStratObj)||Strategy.UPFRONT_OPREP.equals(currStratObj))
			  Collections.sort(allInstances,new InstanceComparatorPerf());
		  
		 //kill B bad instances based on above stratergies
		  for(int i=A;i<A+B;i++)
			  calcPerfStateAndKill(allInstances.get(i), time,true);
	  }
	  
  }
  
  public void simulateNth(int i){
	  int T =simulatorRunParameters.time;
	  int mu = simulatorRunParameters.expectedNoOfReMig;
	  int m = simulatorRunParameters.migrationPenality;
	  int alphaAgg=simulatorRunParameters.alphaAgg;
	  int alphaServ=simulatorRunParameters.alphaServ;
	  int units=simulatorRunParameters.quantum;
	  float delta = 0;
	  
	  double cur_perf = 0;
	  float running_agg_avg = 0;
	  float cur_agg_perf = 0;
	  
	  //work with best A as of now and do opportunistic replacements
//		  System.out.println("Time = "+time/units);
		  delta=mu*(m/units)/(T-i);
		  for(int j=0;j<num_instances;j++){
			  Instance inst=allInstances.get(j);
			  //get the mean from corresponding family/processor type
			  double mean=0;
			  for(CloudDistribution cd : instanceMap.get(inst.family)){
				  if(cd.processor.equalsIgnoreCase(inst.proccessor)){
					  mean=cd.mean;
				  }
			  }
			  
			  if(inst.active==1){
				  if(Strategy.CPU_OPREP.equals(currStratObj)|| Strategy.UPFRONT_OPREP.equals(currStratObj)){
					  switch(currStratObj){
					  case CPU_OPREP:
						  cur_perf=mean;
						  break;
					  case UPFRONT_OPREP:
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
						
						 System.out.println("Migrating type "+ family +" because "+running_agg_avg +" > "+ cur_perf);
						 launch_instance(num_instances+num_migrated, i, time);
						 num_migrated++;
						 calcPerfStateAndKill(inst, time,true);
		
					 }
				  }
				  else if(Strategy.MAX_CPU.equals(currStratObj)){
					  if(inst.family!=null){
						  System.out.println("Migrating type "+ family);
						  launch_instance(num_instances+num_migrated, i, time);
						  num_migrated++;
					      calcPerfStateAndKill(inst, time,true);
					  }
				  }
			  }
		  }
		  num_instances+=num_migrated;
		  time+=units;
	  
  }
  
  public void killAll(){
	  float total_work = 0;
	  int units=simulatorRunParameters.quantum;
	  int T =simulatorRunParameters.time;
	  int A=simulatorRunParameters.A;
	  int B=simulatorRunParameters.B;
	  int mu = simulatorRunParameters.expectedNoOfReMig;
	  int m = simulatorRunParameters.migrationPenality;
	  int alphaAgg=simulatorRunParameters.alphaAgg;
	  int alphaServ=simulatorRunParameters.alphaServ;
	  float aggregate_perf = 0;
	  float naive_total_work = 0;
	  float naive_aggregate_perf = 0;
	  
	  
	//Loop through all of num_instances
	  for(Instance inst : allInstances){
		  
		  if(inst.active==1){
			  calcPerfStateAndKill(inst,time,true);
		  }
		  System.out.println("Instance family= "+ inst.family+"processor= "+inst.proccessor+" total work "+ inst.totalWork);
		  
		  total_work+=inst.totalWork;
	  }
	 
	  System.out.println("Done with current strategy, killing naive instances");
	  time=units*T;
	  for(int i=0;i<A;i++){
		  calcPerfStateAndKill(naiveInstances.get(i), time,true);
		  naive_total_work+=naiveInstances.get(i).totalWork;
	  }
	  
	  aggregate_perf=total_work/(float)((A*T+B)*units);
	  naive_aggregate_perf=naive_total_work/(A*T*units);
	  System.out.println(currStratObj.name()+" "+T+" "+units+" "+A+" "+B+" "+m+" "+mu+" "+alphaAgg+" "+alphaServ);
	  System.out.println("Naive perfs:"+ naive_total_work);  //their code has printed total_work ??
//	  for(Instance inst: naiveInstances) System.out.println(inst.family+" "+inst.id+" "+ inst.avgPerf+" total work -"+inst.totalWork+" total time "+inst.totalTime);
	  System.out.println("Number of instances "+ num_instances);
	  System.out.println("Number migrated "+ (num_instances-A-B));
	  System.out.println("num_migrated = "+num_migrated);
	  System.out.println("First round average+ "+first_avg);
	  System.out.println("Total work "+ total_work);
	  System.out.println("Effective rate "+ aggregate_perf);
	  System.out.println("Naive total work "+ naive_total_work);
	  System.out.println("Naive effective rate"+naive_aggregate_perf);
	  System.out.println("Speedup "+(double)aggregate_perf/(double)naive_aggregate_perf);
	  System.out.println("Percentage improvement "+(double)(aggregate_perf/(double)naive_aggregate_perf-1)*100);
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
		randomFile.close();
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
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
//	  long n1 = 10; 
//	  long n2 = 10;
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
//	  System.out.println("u1===="+u1);
	  float log=(float)Math.log(u1);
//	  System.out.println("log===="+log);
	  x=(float)Math.sqrt(-2*log)*(float)Math.cos(2*PI*u2);
//	  System.out.println("=========="+x);
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
  

  void calcPerfStateAndKill(Instance inst, int time,boolean collaborate){
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
	    
	    //update collaborator module with stats.
	    //TODO this should be updated with the new mean values for each of the SLAs
	    if(collaborate){
		    String combo=inst.family+"-"+inst.proccessor;
		    Collaborator c1=collaboratorMap.get(combo);
		    System.out.println("Collaborator -- Killing instance now. Feeding back performance statistics to the database. Family= "+ inst.family+" Processor= "+inst.proccessor);
		    c1.update(c1.requestsPerSecond, c1.timePerReq, c1.transferRate, c1.concurrency, c1.totalTime);
		    collaboratorMap.put(combo, c1);
	    }
	    
	    System.out.println("Killing instance of type "+inst.family+" id="+inst.id);
	  }

  

  
  /**
   * Launch an instance and update all internal data structures
   * @param cdInstance
   * @param id -> unique id for instance 
   * @param t -> current time unit
   * @param time -> 
   */
  void launch_instance(int id,int t, int time){
	  int threashold = currentCust.collaborateThreashold;
	  int trials=0;
	  
	  String whichProcessor=null;
	  double mean=0;
	  double stddev=0;
	  double runFrac;
	  double cumFrac=0;
	  int quantaForSimulation=this.simulatorRunParameters.time;
	  Instance inst=null;
//	  int idBackup=id;
	
	  while(trials<threashold){
		  //select the instance of the given type randomly
		  long n3 = get_rand();
//		  long n3 = -10;
		  runFrac=(double)(1-(double)n3)/(double)maxRand;
		  for(CloudDistribution cd:instanceMap.get(family)){
			  cumFrac+=cd.fraction;
			  if(runFrac<=cumFrac){
				  whichProcessor=cd.processor;
				  mean = cd.mean;
				  stddev=cd.stddev;
				  break;
			  }
		  }
		  //add this given instance to the instance variable lists. Use collaborator to try and get the best processor type for this family
		  inst= new Instance(id, family, whichProcessor, 1, time, t,currentCust);
		  allInstances.add(inst);
		  String combo=family+"-"+whichProcessor;
		  if(collaboratorMap.get(combo).getRank()!=1) {
			  System.out.println("Collaborator --- Exploring for better processor type . Current processor="+whichProcessor+" current family= "+family+" Current trial =" +trials+" Max trials for this customer= "+ threashold );
			  trials++;
			  if(trials<threashold) {
				  calcPerfStateAndKill(inst, time+simulatorRunParameters.quantum, false);
				  num_instances++;
				  continue;
			  }
		  }
		  else{
			  System.out.println("Collaborator -- Not exploring for better processor.Current processor="+whichProcessor+" current family= "+family+" Current trial =" +trials+" Max trials for this customer= "+ threashold );
			  break;
		  }
	  }
	  
//	  allInstances.add(inst);
	  
	  //set performance parameters
	  for(int i=0;i<quantaForSimulation;i++){
		  inst.perf[i]=stddev*gen_std_normal()+mean;
	  }
	  inst.curPerf=inst.perf[t];
	  System.out.println("Launching instance of family "+family+", processor"+whichProcessor+" id "+id+"Performance of launched instance "+inst.curPerf);
  }
  
  
  public static void main(String args[]){
//	  PredictFamily MLObj = new PredictFamily("custInfo.csv", "custInfoAfterPrediction.csv");
//	  List<Customer> customerInfoList=Helper.getCustomerInfo(MLObj.getOutputFilename());
	  
	  HashMap<String,List<CloudDistribution>> instanceMap=Helper.getDistribution("ner1-config");
	  List<Customer> customerInfoList=Helper.getCustomerInfo("custInfoAfterPrediction.csv");
	  RunParams simulatorRunParameters=Helper.getRunParams("runConfig.prop");
	  HashMap<String,List<Integer>> custBasedOnClass = Helper.getClassifiedCust(customerInfoList);
	  HashMap<String,Collaborator> collaboratorMap = Helper.getCollaboratorPerfStats("customerPerfStats.csv");
	  
	  int T=simulatorRunParameters.time;
	  int units=simulatorRunParameters.quantum;
	  List<Simulator> simObjList = new ArrayList<Simulator>(customerInfoList.size());
	  
	  for(int i=0;i<customerInfoList.size();i++){
		  Simulator sim = new Simulator(instanceMap,simulatorRunParameters,Strategy.values()[simulatorRunParameters.strategy].toString(),customerInfoList.get(i),custBasedOnClass,collaboratorMap);
		  simObjList.add(i,sim);
	  }
	  
	  //execute 0th quantum for all customers
	  for(int i=0;i< customerInfoList.size();i++){
		  Simulator sim = simObjList.get(i);
		  sim.simulateZero();
	  } 
	  
	  //execute nth quantum for all customers one by one
	  for(int j=1;j<T-1;j++){
		  System.out.println("Time===="+j);
		  for(int i=0;i< customerInfoList.size();i++){
			  System.out.println("cust===="+i);
			  Simulator sim = simObjList.get(i);
			  if(Strategy.CPU_OPREP.equals(sim.currStratObj)|| Strategy.UPFRONT_OPREP.equals(sim.currStratObj)|| Strategy.MAX_CPU.equals(sim.currStratObj)){
					  sim.simulateNth(j);
					  sim.time+=units;
			  }else{
				  sim.time+=units*(T-1);
			  }
		  }
	  }
	  //execute last quantum for all customers
	  for(int i=0;i< customerInfoList.size();i++){
		  Simulator sim = simObjList.get(i); 
		  sim.killAll();
	  }
	  
  }
}

