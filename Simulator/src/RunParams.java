
public class RunParams {
	int strategy;
	int time;
	int quantum;
	int A;
	int B;
	int migrationPenality;
	int expectedNoOfReMig;
	int alphaAgg;
	int alphaServ;
	
	RunParams(int strategy,int time,int quantum,int A,int B,int migrationPenality,int expectedNoOfReMig,int alphaAgg,int alphaServ){
		this.strategy=strategy;
		this.time=time;
		this.quantum=quantum;
		this.A=A;
		this.B=B;
		this.migrationPenality=migrationPenality;
		this.expectedNoOfReMig=expectedNoOfReMig;
		this.alphaAgg=alphaAgg;
		this.alphaServ=alphaServ;
	}
	public int getStrategy() {
		return strategy;
	}
	public void setStrategy(int strategy) {
		this.strategy = strategy;
	}
	public int getTime() {
		return time;
	}
	public void setTime(int time) {
		this.time = time;
	}
	public int getQuantum() {
		return quantum;
	}
	public void setQuantum(int quantum) {
		this.quantum = quantum;
	}
	public int getA() {
		return A;
	}
	public void setA(int a) {
		A = a;
	}
	public int getB() {
		return B;
	}
	public void setB(int b) {
		B = b;
	}
	public int getMigrationPenality() {
		return migrationPenality;
	}
	public void setMigrationPenality(int migrationPenality) {
		this.migrationPenality = migrationPenality;
	}
	public int getExpectedNoOfReMig() {
		return expectedNoOfReMig;
	}
	public void setExpectedNoOfReMig(int expectedNoOfReMig) {
		this.expectedNoOfReMig = expectedNoOfReMig;
	}
	public int getAlphaAgg() {
		return alphaAgg;
	}
	public void setAlphaAgg(int alphaAgg) {
		this.alphaAgg = alphaAgg;
	}
	public int getAlphaServ() {
		return alphaServ;
	}
	public void setAlphaServ(int alphaServ) {
		this.alphaServ = alphaServ;
	}
	
	public String toString() {
	return(String.valueOf(this.strategy));
	}
}
