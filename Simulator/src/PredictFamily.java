

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;


public class PredictFamily {
	private String outputFilename;
	
	public PredictFamily(String customerInfoFile, String outputFile) {
		//python module expects : concurrency,time,reqpersec,timeperreqall,timerperreq,trasrate
		//customer Info csv File : id, class, concurrency,time,reqpersec,timerperreq,transrate
		//timeperreqall = concurrency * timeperreq
		
		//1) First read in customerInfoFile
		
		//2) Write in test data format
		
		//3) Call/Load python predict script
		this.setOutputFilename(outputFile);
		String s = null;
		Process process=null;
		try {
			//process = Runtime.getRuntime().exec("python pickleLoad.py custInfo.csv custInfoAfterPrediction.csv");
			process = Runtime.getRuntime().exec("python pickleLoad.py " + customerInfoFile + " " + this.outputFilename);
			//process = Runtime.getRuntime().exec("ls");
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
			while ((s = stdInput.readLine()) != null) {
			   System.out.println(s);
			}
			} catch (IOException e) {
			e.printStackTrace();
			}
			   return;
			  }

	public String getOutputFilename() {
		return outputFilename;
	}

	public void setOutputFilename(String outputFilename) {
		this.outputFilename = outputFilename;
	}
		
		//4) Get the resultant csv file with predicted results
		
		//Pass this csv filename back to Simulator class
 			
	}


