import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Random;

enum stratergy{
  CPU,
  UPFRONT,
  UPFRONT_PREP,
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
  
  Simulator(String distributionFile,String runParamsFile,String customerFile){
	  allInstances=new ArrayList<Instance>();
	  naiveInstances=new ArrayList<Instance>();
	  instanceMap=getDistribution(distributionFile);
	  
//	  for (Entry<String, List<CloudDistribution>> entry : instanceMap.entrySet()) { 
//	  System.out.println(entry.getKey() + entry.getValue()); for (CloudDistribution
//	  eachInstance : entry.getValue()) { System.out.println(eachInstance.toString()); } }
	  
	 customerInfoList=getCustomerInfo(customerFile);
	  
// 	 for (Customer eachCustomer : customerInfoList) { System.out.println(eachCustomer.toString()); }
		 
	 simulatorRunParameters=getRunParams(runParamsFile);
//  	 System.out.println(simulatorRunParameters.toString());
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
  
  /*mfm modules*/
  void simulate(String strategy, int A, int B){
   
  }

  /**
   * 
   * @return
   */
  float gen_std_normal(){
	  float u1,u2,x,r;
	  
	  Random rand=new Random();
	  u1=rand.nextInt(0)/(float)maxRand;
	  u2=rand.nextInt(0)/(float)maxRand;
	  
	  float log=(float)Math.log(u1)/(float)Math.log(2);
	  x=(float)Math.sqrt(-2*log)*(float)Math.acos(2*Math.PI*u2);
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
	    inst.avgPerf=inst.totalWork/inst.totalTime;
	    System.out.println("Killing instance of type "+inst.family+" id="+inst.id);
	  }
  
  /**
   * Launch an instance and update all internal data structures
   * @param cdInstance
   * @param id -> unique id for instance 
   * @param t -> current time unit
   * @param time -> not sure ??
   */
  void launch_instance(CloudDistribution cdInstance,int id,int t, int time){
	  String whichFamily=cdInstance.type;
	  String whichProcessor=null;
	  double runFrac;
	  double cumFrac=0;
	  int quantaForSimulation=this.simulatorRunParameters.time;
	  double mean = cdInstance.mean;
	  double stddev=cdInstance.stddev;
	  //TODO check if no of instances is greater than max possible instances
	  
	  //select the instance of the given type randomly
	  Random rand= new Random();
	  int randomNum = rand.nextInt();
	  runFrac=(1-randomNum)/maxRand;
	  for(CloudDistribution cd:instanceMap.get(whichFamily)){
		  cumFrac+=cd.fraction;
		  if(runFrac<=cumFrac){
			  whichProcessor=cd.processor;
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
	  Simulator sim = new Simulator("vmTypes.csv", "runConfig.prop", "custInfo.csv");
    
    //read file for cloud distribution + create instances
    
    //read the strategy prop file 
    
    //read SLA prop file 
    
    //call the ML module get the instance type
    
    //pass ML output as simulator input 
    
    //perform simulation based on strategy -> switch 
    
    //cleanup
  }
  
}
