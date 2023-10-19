package ocha.itolab.koala.batch.py4j;

import java.util.ArrayList;
import java.io.*;
import ocha.itolab.koala.core.data.*;
import ocha.itolab.koala.core.forcedirected.LinLogLayout;
import ocha.itolab.koala.core.forcedirected.PersistentHomology;
import ocha.itolab.koala.core.mesh.*;
import ocha.itolab.koala.evaluate.sprawlter.*;
import java.util.Map;
import java.util.HashMap;

public class KoalaToSprawlter {
	static String infile = Constants.Path.DATA_CSV;
	static String outfiledir = Constants.Path.RESULT;
	static Graph graph;
	static int SMOOTHING_ITERATION = 100;
	static int NUM_PER_GENERATION = 20;
	static double nnmax = 0.4, nemax = 1930.0, eemax = 60000.0;
//	static double NN_RATIO = 1.0, NE_RATIO = 1.0, EE_RATIO = 0.5;
//	static double NN_RATIO = 0.5, NE_RATIO = 0.5, EE_RATIO = 1.0;
	static double NN_RATIO = 1.0, NE_RATIO = 1.0, EE_RATIO = 1.0;
	
	/**
	 * Execute Koala and Sprawlter
	 */
	public static Map<String, Double> execute(double init[], int method) {
		double sprawlter = 0.0;
//		System.out.println("generate initial position list");
		// LinLogLayoutクラスのinitialPosを設定
		generateInitPositionList(init);
//		System.out.println("read connectivity");
		graph = GraphFileReader.readConnectivity(infile, method);
//		System.out.println("generate edges");
		graph.generateEdges();
//		System.out.println("generate mesh");
		for(int i = 0; i < SMOOTHING_ITERATION; i++) {
			MeshTriangulator.triangulate(graph.mesh);
			boolean ret = MeshSmoother.smooth(graph.mesh, graph.maxDegree, 0.05);
		}
		graph.mesh.finalizePosition();

//		System.out.println("generate layout");
		
		writeLayoutFile(graph);

		SprawlterEvaluator.calcNodeNodePenalty(graph, 1);
		SprawlterEvaluator.calcNodeEdgePenalty(graph, 1);

//		System.out.println("sprawlter evaluation");
		// Sprawlの算出式
		double sprawl = SprawlterEvaluator.calcSprawl(graph);
		System.out.println(String.format("sprawl: %f", sprawl));

		double nnpen = SprawlterEvaluator.calcNodeNodePenalty(graph, 2);
		double nepen = SprawlterEvaluator.calcNodeEdgePenalty(graph, 2);
		double eepen = SprawlterEvaluator.calcEdgeEdgePenalty(graph);

//		System.out.println("clutter evaluation");
		// Clutterの算出式
		double clutter = NN_RATIO * nnpen / nnmax + NE_RATIO * nepen / nemax + EE_RATIO * eepen / eemax;
		System.out.println(String.format("nnpen: %f, nepen: %f, eepen: %f", nnpen, nepen, eepen));
		System.out.println(String.format("clutter: %f", clutter));
		
		nnpen = Math.sqrt(sprawl * nnpen / nnmax);
		nepen = Math.sqrt(sprawl * nepen / nemax);
		eepen = Math.sqrt(sprawl * eepen / eemax);
		
		sprawlter = NN_RATIO * nnpen + NE_RATIO * nepen + EE_RATIO * eepen; 
		System.out.println(String.format("--------- %f ", sprawlter));
		
		// sprawl, clutter, sprawlter 全てを返す
		Map<String, Double> results = new HashMap<String, Double>();
		results.put("sprawl", sprawl);
		results.put("clutter", clutter);
		results.put("sprawlter", sprawlter);

		return results;
	}
	
	
	static void generateInitPositionList(double init[]) {
		ArrayList<double[]> poslist = new ArrayList<double[]>();
		for(int i = 0; i < init.length; i += 2) {
			double pos[] = new double[3];
			pos[0] = init[i] * 0.1;
			pos[1] = init[i + 1] * 0.1;
			pos[2] = 0.0;
			poslist.add(pos);
		}
		// LinLogLayout.setInitialPositionList(poslist);
		PersistentHomology.setInitialPositionList(poslist);
	}

	
	static void writeLayoutFile(Graph graph) {
		String filename = "";
		
		try {
			File dir = new File(outfiledir);
			for(int i = 0;;i++) {
				for(int j = 0; j < NUM_PER_GENERATION; j++) {
					filename = outfiledir + "/layout" + i + "-" + j + ".csv";
					File file = new File(filename);
					if(file.exists() == true) continue;
					LayoutFileWriter.write(graph, filename);
					return;
				}
			}
			
			
		} catch(Exception e) {
			e.printStackTrace();
		}
		
		LayoutFileWriter.write(graph, filename);
	}
	
}
