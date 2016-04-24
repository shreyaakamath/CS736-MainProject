import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Random;

enum Stratergy{
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

public class Simulator {
  RunParams simulatorRunParameters;
  HashMap<String,List<CloudDistribution>> instanceMap;
  List<Customer> customerInfoList;
  HighLevelSla sla;
  List<Instance> allInstances;
  List<Instance> naiveInstances;
  static long maxRand = 4294967295l;
  List<Customer> allCustomer;
  int random1 =11;
  int random2 =21;
  
  Simulator(String distributionFile,String runParamsFile,String customerFile){
	  allInstances=new ArrayList<Instance>();
	  naiveInstances=new ArrayList<Instance>();
	  
	 instanceMap=getDistribution(distributionFile);
	 customerInfoList=getCustomerInfo(customerFile);
	 simulatorRunParameters=getRunParams(runParamsFile);
  	 
  }

public void test(){
	  for (Entry<String, List<CloudDistribution>> entry : instanceMap.entrySet()) { 
	  System.out.println(entry.getKey() + entry.getValue()); for (CloudDistribution
	  eachInstance : entry.getValue()) { System.out.println(eachInstance.toString()); } }
	for (Customer eachCustomer : customerInfoList) { System.out.println(eachCustomer.toString()); }
	System.out.println(simulatorRunParameters.toString());
}
  
public static HashMap<String, List<CloudDistribution>> getDistribution(String distributionFile) {
	// Row format is : type,processor,fraction,mean,stddev
	HashMap<String, List<CloudDistribution>> instanceMap = new HashMap<String, List<CloudDistribution>>();
	String csvFile = distributionFile;
	BufferedReader br = null;
	String line = "";
	String cvsSplitBy = ",";
	CloudDistribution eachInstance = null;
	String type, processor;
	double fraction, mean, stdDev;

	try {
		br = new BufferedReader(new FileReader(csvFile));
		while ((line = br.readLine()) != null) {
			// use comma as separator
			String[] row = line.split(cvsSplitBy);
			type = String.valueOf(row[0]);
			processor = String.valueOf(row[1]);
			fraction = Double.parseDouble(row[2]);
			mean = Double.parseDouble(row[3]);
			stdDev = Double.parseDouble(row[4]);
			eachInstance = new CloudDistribution(type, processor, fraction, mean, stdDev);
			if(instanceMap.get(type) != null) {
				instanceMap.get(type).add(eachInstance);
				}
			else
				{
				List<CloudDistribution> instancesInATypeList = new ArrayList<CloudDistribution>();
				instancesInATypeList.add(eachInstance);
				instanceMap.put(type, instancesInATypeList);
				}
			}
		}
	catch(FileNotFoundException e) {
		e.printStackTrace();
		}
	catch(IOException e) {
		e.printStackTrace();
		}
	finally {
		if(br != null)
			{
			try
				{
				br.close();
				}
			catch(IOException e)
				{
				e.printStackTrace();
				}
			}
		}
	return instanceMap;

	}

public static List<Customer> getCustomerInfo(String customerInfoFile)
	{
	// id, class, reqPerSec, concurrency, timePerReq, transferRate, totalTime
	HighLevelSla custSLA = null;
	Customer eachCustomer = null;
	List<Customer> custInfoList = new ArrayList<Customer>();
	String csvFile = customerInfoFile;
	BufferedReader br = null;
	String line = "";
	String cvsSplitBy = ",";

	double reqPerSecond;
	double timePerReq;
	double transferRate;
	int concurrency;
	int totalTime;

	int id;
	HighLevelSla sla;
	String custClass;

	try
		{
		br = new BufferedReader(new FileReader(csvFile));
		while ((line = br.readLine()) != null)
			{
			// use comma as separator
			String[] row = line.split(cvsSplitBy);
			//System.out.println(line);
			//System.out.println(row[0] + " " + row[1] + " " + row[2] + " " + row[3] + " " + row[4] + " " + row[5] + " " + row[6]);
			id = Integer.parseInt(row[0]);
			custClass = row[1];
			reqPerSecond = Double.parseDouble(row[2]);
			concurrency = Integer.parseInt(row[3]);
			timePerReq = Double.parseDouble(row[4]);
			transferRate = Double.parseDouble(row[5]);
			totalTime = Integer.parseInt(row[6]);

			custSLA = new HighLevelSla(reqPerSecond, timePerReq, transferRate, concurrency, totalTime);
			eachCustomer = new Customer(id, custSLA, custClass);
			custInfoList.add(eachCustomer);
			}
		}
	catch(FileNotFoundException e)
		{
		e.printStackTrace();
		}
	catch(IOException e)
		{
		e.printStackTrace();
		}
	finally
		{
		if(br != null)
			{
			try
				{
				br.close();
				}
			catch(IOException e)
				{
				e.printStackTrace();
				}
			}
		}
	return custInfoList;
	}

public static RunParams getRunParams(String runParamsFile)
	{
	int strategy;
	int time;
	int quantum;
	int A;
	int B;
	int migrationPenality;
	int expectedNoOfReMig;
	int alphaAgg;
	int alphaServ;
	RunParams simulatorRunParameters = null;
	try
		{
		Properties prop = new Properties();
		prop.load(new FileInputStream(runParamsFile));
		
		strategy = Integer.parseInt(prop.getProperty("strategy"));
		time = Integer.parseInt(prop.getProperty("time"));
		quantum = Integer.parseInt(prop.getProperty("quantum"));
		A = Integer.parseInt(prop.getProperty("A"));
		B = Integer.parseInt(prop.getProperty("B"));
		migrationPenality = Integer.parseInt(prop.getProperty("migrationPenality"));
		expectedNoOfReMig = Integer.parseInt(prop.getProperty("expectedNoOfReMig"));
		alphaAgg = Integer.parseInt(prop.getProperty("alphaAgg"));
		alphaServ = Integer.parseInt(prop.getProperty("alphaServ"));
		simulatorRunParameters = new RunParams(strategy, time, quantum,  A, B, migrationPenality, expectedNoOfReMig, alphaAgg, alphaServ);
		}
	catch(Exception e)
		{
		e.printStackTrace();
		}
	return simulatorRunParameters;
	}

  /*from scratch*/
  void collaborator(){
    
  }
  
  void feedback(){
    
  }

  void ML(){
	    
  }
  
  void simulate(String strat, String family){
	  
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
	  
	  Stratergy s= Stratergy.valueOf(strat);
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
	  /*naiveInstances=new ArrayList<Instance>();
	  for(Instance inst:allInstances){
		  Instance i1 = new Instance(inst.id, inst.family, inst.proccessor, inst.active, inst.startTime, inst.startQuantum);
		  naiveInstances.add(i1);
	  }*/
	  naiveInstances= new ArrayList<Instance>(allInstances);
	  int units=simulatorRunParameters.quantum;
	  time+=units;
	  
	  //end up-front exploration
	  if(T>0 && B>0){
		  if(Stratergy.CPU.equals(s)|| Stratergy.MAX_CPU.equals(s))
			  Collections.sort(allInstances,new InstanceComparatorType());
		  else if (Stratergy.UPFRONT.equals(s)||Stratergy.UPFRONT_OPREP.equals(s))
			  Collections.sort(allInstances,new InstanceComparatorPerf());
		  
		 //kill B bad instances based on above stratergies
		  for(int i=A;i<A+B;i++)
			  kill_instance(allInstances.get(i), time);
	  }
	  
	  //work with best A as of now and do opportunistic replacements
	  if(Stratergy.CPU_OPREP.equals(s)|| Stratergy.UPFRONT_OPREP.equals(s)|| Stratergy.MAX_CPU.equals(s)){
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
					  if(Stratergy.CPU_OPREP.equals(s)|| Stratergy.UPFRONT_OPREP.equals(s)){
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
							  inst.cufPerf=alphaServ * inst.perf[i]+(1-alphaServ)*allInstances.get(j-1).cufPerf;
							  cur_perf=inst.cufPerf;
							  break;
						default:
							System.out.println("error unknown strategy ");
							break;
						  }
						  
						 if(running_agg_avg - cur_perf > delta){
							 System.out.println("Migrating type "+ family +" because "+running_agg_avg +" > "+ cur_perf);
							 launch_instance(family, num_instances+num_migrated, i, time);
							 num_migrated++;
							 kill_instance(inst, time);
						 }
					  }
					  else if(Stratergy.MAX_CPU.equals(s)){
						  if(inst.family!=null){
							  System.out.println("Migrating type "+ family);
							  launch_instance(family, num_instances+num_migrated, i, time);
							  num_migrated++;
						      kill_instance(inst, time);
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
			  kill_instance(inst, time);
		  }
		  System.out.println("inst total work "+ inst.totalWork);
		  total_work+=inst.totalWork;
	  }
	 
	  System.out.println("done with current strategy, killing naive instances");
	  time=units*T;
	  for(int i=0;i<A;i++){
		  kill_instance(naiveInstances.get(i), time);
		  naive_total_work+=naiveInstances.get(i).totalWork;
	  }
	  
	  aggregate_perf=total_work/(float)((A*T+B)*units);
	  naive_aggregate_perf=naive_total_work/(A*T*units);
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
	  System.out.println("Speedup "+aggregate_perf/naive_aggregate_perf);
	  System.out.println("Percentage improvement "+(aggregate_perf/naive_aggregate_perf-1)*100);
  }

long get_rand(){
	  long result = 0;
	  try {
		FileInputStream randomFile = new FileInputStream("/dev/urandom");
		long ret;
		int numread = 102;
		byte[] data = new byte[4]; 
		try {
			randomFile.read(data);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if(data !=  null)
		{
			//System.out.println(data);
			result = ByteBuffer.wrap(data).getInt();
			System.out.println(result);
			//return (int)data;
		}
	} catch (FileNotFoundException e) {
		// TODO Auto-generated catch block
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
	  u1=n1/(float)maxRand;
	  System.out.println("U1 random = " + n1);
	  long n2 = get_rand();
	  u2=n2/(float)maxRand;
	  System.out.println("U2 random = " + n2);
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
  /**
   * 
   * @param inst -> instance to be killed
   * @param time -> current time
   */
  void kill_instance(Instance inst, int time){
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
	  //Random rand= new Random();
	  //int randomNum = rand.nextInt();
	  //int randomNum=31;
	  long n3 = get_rand();
	  System.out.println("runFrac random = " + n3);
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
	  Instance inst= new Instance(id, whichFamily, whichProcessor, 1, time, t);
	  allInstances.add(inst);
	  
	  //TODO bimodal frac 
	  
	  //set performance parameters
	  for(int i=0;i<quantaForSimulation;i++){
		  inst.perf[i]=stddev*gen_std_normal()+mean;
	  }
	  inst.cufPerf=inst.perf[t];
	  
	  //print info
	  System.out.println("Launching instance of family "+whichFamily+", processor"+whichProcessor+" id "+id+"Performance of launched instance "+inst.cufPerf);
  }
  

  public static void main(String args[]){
	  //get_rand();
	  Simulator sim = new Simulator("ner1-config", "runConfig.prop", "custInfo.csv");
	  sim.simulate("CPU", "micro");
    
    //read file for cloud distribution + create instances
    
    //read the strategy prop file 
    
    //read SLA prop file 
    
    //call the ML module get the instance type
    
    //pass ML output as simulator input 
    
    //perform simulation based on strategy -> switch 
    
    //cleanup
  }
  
}
