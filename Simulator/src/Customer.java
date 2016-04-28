public class Customer{
	int id;
	HighLevelSla sla;
	String custClass;
	String predictedFamily;
	int collaborateThreashold;
	  
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public HighLevelSla getSla() {
		return sla;
	}

	public void setSla(HighLevelSla sla) {
		this.sla = sla;
	}

	public String getCustClass() {
		return custClass;
	}

	public void setCustClass(String custClass) {
		this.custClass = custClass;
	}

	public String getPredictedFamily() {
		return predictedFamily;
	}

	public void setPredictedFamily(String predictedFamily) {
		this.predictedFamily = predictedFamily;
	}
		
  public Customer(int id, HighLevelSla sla, String custClass,String predicted,int collaborateThreashold) {
	super();
	this.id = id;
	this.sla = sla;
	this.custClass = custClass;
	this.predictedFamily=predicted;
	this.collaborateThreashold=collaborateThreashold;
}
  public String toString() {
		return("Id: " + this.id + " SLA: " + this.sla + " Class: " + this.custClass);
	}

}