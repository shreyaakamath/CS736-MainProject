
public class HighLevelSla {
	double requestsPerSecond;
	double timePerReq;
	double transferRate;
	double concurrency;
	double totalTime;
	  
	public HighLevelSla(double requestsPerSecond, double timePerReq,
			double transferRate, double concurrency,double totalTime) {
		super();
		this.requestsPerSecond = requestsPerSecond;
		this.timePerReq = timePerReq;
		this.transferRate = transferRate;
		this.concurrency = concurrency;
		this.totalTime=totalTime;
	}
	
	public double getRequestsPerSecond() {
		return requestsPerSecond;
	}
	public void setRequestsPerSecond(double requestsPerSecond) {
		this.requestsPerSecond = requestsPerSecond;
	}
	public double getTimePerReq() {
		return timePerReq;
	}
	public void setTimePerReq(double timePerReq) {
		this.timePerReq = timePerReq;
	}
	public double getTransferRate() {
		return transferRate;
	}
	public void setTransferRate(double transferRate) {
		this.transferRate = transferRate;
	}
	public double getConcurrency() {
		return concurrency;
	}
	public void setConcurrency(double concurrency) {
		this.concurrency = concurrency;
	}
	
	
}
