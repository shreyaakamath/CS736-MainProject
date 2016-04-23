import java.util.Comparator;


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
	double cufPerf;
	double perf[];//max time quantum
	
	public Instance(int id, String family,String processor, int active, int startTime,
			int startQuantum ) {
		super();
		this.id = id;
		this.family= family;
		this.proccessor=processor;
		this.active = active;
		this.startTime = startTime;
		this.startQuantum = startQuantum;
		perf=new double[1000];
	}
	
	
}

class InstanceComparatorPerf implements Comparator<Instance>{
	public int compare(Instance i1, Instance i2){
		double p1=i1.perf[0];
		double p2=i1.perf[0];
		if(p1 > p2) return 1;
		else if (p1<p2) return -1;
		else return 0;
	}
	
}

// TODO compare customer by type