
public class Collaborator {
	
	
	int rank;
	double requestsPerSecond;
	double timePerReq;
	double transferRate;
	double concurrency;
	double totalTime;
	
	public Collaborator(int rank,
			double requestsPerSecond, double timePerReq, double transferRate,
			double concurrency, double totalTime) {
		super();
		this.rank = rank;
		this.requestsPerSecond = requestsPerSecond;
		this.timePerReq = timePerReq;
		this.transferRate = transferRate;
		this.concurrency = concurrency;
		this.totalTime = totalTime;
	}
	public int getRank() {
		return rank;
	}

	public void setRank(int rank) {
		this.rank = rank;
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

	public double getTotalTime() {
		return totalTime;
	}

	public void setTotalTime(double totalTime) {
		this.totalTime = totalTime;
	}

	public void update(double requestsPerSecond, double timePerReq, double transferRate,
			double concurrency, double totalTime){
		
	}
}
