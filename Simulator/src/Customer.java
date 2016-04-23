public class Customer{
	int id;
	HighLevelSla sla;
	String custClass;
	  
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

	
  public Customer(int id, HighLevelSla sla, String custClass) {
	super();
	this.id = id;
	this.sla = sla;
	this.custClass = custClass;
}
  public String toString() {
		return("Id: " + this.id + " SLA: " + this.sla + " Class: " + this.custClass);
	}

}