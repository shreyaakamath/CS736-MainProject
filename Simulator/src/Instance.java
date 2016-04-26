import java.util.Comparator;
import java.util.HashMap;


public class Instance {
	int id;
	String family;
	String proccessor;
	int active;
	int startTime;
	int startQuantum;
	int endTime;
	int totalTime;
	double totalTimeComputation;
	int totalWork;
	float avgPerf;
	double curPerf;
	double perf[];//max time quantum
	int customerId;
	
	public Instance(int id, String family,String processor, int active, int startTime,
			int startQuantum , int custId) {
		super();
		this.id = id;
		this.family= family;
		this.proccessor=processor;
		this.active = active;
		this.startTime = startTime;
		this.startQuantum = startQuantum;
		perf=new double[1000];
		this.customerId=custId;
	}
	
}

class InstanceComparatorPerf implements Comparator<Instance>{
	public int compare(Instance i1, Instance i2){
		double p1=i1.perf[0];
		double p2=i1.perf[0];
		if(p1 > p2) return -1;
		else if (p1<p2) return 1;
		else return 0;
	}
}

class InstanceComparatorType implements Comparator<Instance>{
	HashMap<String,Integer> rankFamily;
	InstanceComparatorType(){
		rankFamily = new HashMap<String,Integer>();
		rankFamily.put("nano", 1);
		rankFamily.put("micro", 1);
		rankFamily.put("small", 1);
	}
	
	public int compare(Instance i1, Instance i2){
		int rank1=0;
		int rank2=0;
		try{
			rank1=rankFamily.get(i1.family);
			rank2=rankFamily.get(i2.family);
		}catch(Exception e){
			System.out.println(e.toString());
			System.out.println("The acceptable family types are nano, micro , small . Is the simulator instance config correct?");
		}
		if(rank1 > rank2) return 1;
		else if (rank1<rank2) return -1;
		else return 0;
	}
}
// TODO compare customer by type