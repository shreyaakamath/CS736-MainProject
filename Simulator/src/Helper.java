import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

class Helper {

	public static HashMap<String, List<Integer>> getClassifiedCust(
			List<Customer> all) {
		HashMap<String, List<Integer>> map = new HashMap<String, List<Integer>>();
		for (Customer c : all) {
			String custClass = c.custClass;
			if (map.containsKey(custClass)) {
				List<Integer> list = map.get(custClass);
				list.add(c.id);
				map.put(custClass, list);
			} else {
				List<Integer> list = new ArrayList<Integer>();
				list.add(c.id);
				map.put(custClass, list);
			}
		}
		return map;
	}

	public static HashMap<String, List<CloudDistribution>> getDistribution(
			String distributionFile) {
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
				eachInstance = new CloudDistribution(type, processor, fraction,
						mean, stdDev);
				if (instanceMap.get(type) != null) {
					instanceMap.get(type).add(eachInstance);
				} else {
					List<CloudDistribution> instancesInATypeList = new ArrayList<CloudDistribution>();
					instancesInATypeList.add(eachInstance);
					instanceMap.put(type, instancesInATypeList);
				}
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return instanceMap;

	}

	public static List<Customer> getCustomerInfo(String customerInfoFile) {
		// id, class, concurrency,time,reqpersec,timerperreq,transrate

		HighLevelSla custSLA = null;
		Customer eachCustomer = null;
		List<Customer> custInfoList = new ArrayList<Customer>();
		String csvFile = customerInfoFile;
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";
		String predictedFamily;

		double reqPerSecond;
		double timePerReq;
		double transferRate;
		double concurrency;
		double totalTime;

		int id;
		HighLevelSla sla;
		String custClass;
		try {
			br = new BufferedReader(new FileReader(csvFile));
			while ((line = br.readLine()) != null) {
				// use comma as separator
				String[] row = line.split(cvsSplitBy);
				// System.out.println(line);
				// System.out.println(row[0] + " " + row[1] + " " + row[2] + " "
				// + row[3] + " " + row[4] + " " + row[5] + " " + row[6] + " " +
				// row[7]);
				id = Integer.parseInt(row[0]);
				custClass = row[1];
				concurrency = Double.parseDouble(row[2]);
				totalTime = Double.parseDouble(row[3]);
				reqPerSecond = Double.parseDouble(row[4]);
				timePerReq = Double.parseDouble(row[5]);
				transferRate = Double.parseDouble(row[6]);
				predictedFamily = row[7];
				custSLA = new HighLevelSla(reqPerSecond, timePerReq,
						transferRate, concurrency, totalTime);
				eachCustomer = new Customer(id, custSLA, custClass,
						predictedFamily);
				custInfoList.add(eachCustomer);
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return custInfoList;
	}

	public static RunParams getRunParams(String runParamsFile) {
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
		try {
			Properties prop = new Properties();
			prop.load(new FileInputStream(runParamsFile));

			strategy = Integer.parseInt(prop.getProperty("strategy"));
			time = Integer.parseInt(prop.getProperty("time"));
			quantum = Integer.parseInt(prop.getProperty("quantum"));
			A = Integer.parseInt(prop.getProperty("A"));
			B = Integer.parseInt(prop.getProperty("B"));
			migrationPenality = Integer.parseInt(prop
					.getProperty("migrationPenality"));
			expectedNoOfReMig = Integer.parseInt(prop
					.getProperty("expectedNoOfReMig"));
			alphaAgg = Integer.parseInt(prop.getProperty("alphaAgg"));
			alphaServ = Integer.parseInt(prop.getProperty("alphaServ"));
			simulatorRunParameters = new RunParams(strategy, time, quantum, A,
					B, migrationPenality, expectedNoOfReMig, alphaAgg,
					alphaServ);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return simulatorRunParameters;
	}
}
