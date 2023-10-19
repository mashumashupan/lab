package ocha.itolab.koala.batch.py4j;
import py4j.GatewayServer;
import java.util.Map;
import java.util.HashMap;

public class ObjectFunction{
	private double[] _arr = new double[460*2];
	private double[] _result = new double[3];

	public double[] obfunc(double val, int current, int finish, int method) {
		// store values
		_arr[current] = val;

		if (current == finish - 1){
			// execute KoalaToSprawlter
//			System.out.println("execute KoalaToSprawlter");
			Map<String, Double> results_map = KoalaToSprawlter.execute(_arr, method);
			_result[0] = results_map.get("sprawl");
			_result[1] = results_map.get("clutter");
			_result[2] = results_map.get("sprawlter");

			return _result;
		}

		return _result;
	}
	
	public static void main(String[] args) {
		ObjectFunction app = new ObjectFunction();
		GatewayServer server = new GatewayServer(app);
		server.start();
		System.out.println("Gateway Server Started");
	}
}
