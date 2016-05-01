public class CloudDistribution {
	String type;
	String processor;
	double fraction;
	double mean;
	double stddev;
	
	CloudDistribution(String type, String processor, double fraction, double mean, double stddev){
	  this.type = type;
	  this.processor = processor;
	  this.fraction = fraction;
	  this.mean = mean;
	  this.stddev = stddev;
	}
	
	public String getType(){
	  return this.type;
	}
	
	public String getProcessor(){
	  return this.processor;
	}
	
	public double getFraction(){
	  return this.mean;
	}
	
	public double getStdDev(){
	  return this.stddev;
	}
	
	public String toString() {
		return ("Type: " + this.type + " Processor: " + this.processor + " Fraction:  " + this.fraction + " Mean: " + this.mean + " Std Dev: " + this.stddev);
	}
}