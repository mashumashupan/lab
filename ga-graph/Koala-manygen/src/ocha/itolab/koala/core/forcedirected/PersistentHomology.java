package ocha.itolab.koala.core.forcedirected;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.StringTokenizer;
import java.util.Vector;

import usf.dvl.graph.Graph;
import usf.dvl.graph.layout.forcedirected.*;

/**
 * @author Andreas Noack (an@informatik.tu-cottbus.de)
 * @version 14.01.2008
 */
public class PersistentHomology {

	// 遺伝子情報
	static ArrayList<double[]> initialpos = null;
	public static void setInitialPositionList(ArrayList<double[]> list) {
		initialpos = list;
	}
	
	public static Graph constructGraph(Vector edgelist, ArrayList<double[]> positions) {
		Graph result = new Graph();

		// add nodes
		for(int i = 0; i < positions.size(); i++) {
			result.addVertex();
		}
//		System.out.println(result.getNodeCount() + " nodes");
//		System.out.println("edgelist.size() = " + edgelist.size());
		for(int i = 0; i < edgelist.size(); i++) {
			InputEdge ie = (InputEdge)edgelist.elementAt(i);
			result.addEdge(ie.node1, ie.node2, ie.weight);
		}
		return result;
	}
	
	/**
	 * @param graph  possibly unsymmetric graph.
	 * @return symmetric version of the given graph.
	 */
	public static Map<String,Map<String,Double>> makeSymmetricGraph(Map<String,Map<String,Double>> graph) {
		Map<String,Map<String,Double>> result = new HashMap<String,Map<String,Double>>();
		for (String source : graph.keySet()) {
			for (String target : graph.get(source).keySet()) {
				double weight = graph.get(source).get(target);
				double revWeight = 0.0f;
				if (graph.get(target) != null && graph.get(target).get(source) != null) {
					revWeight = graph.get(target).get(source);
				}
				if (result.get(source) == null) result.put(source, new HashMap<String,Double>());
				result.get(source).put(target, weight+revWeight);
				if (result.get(target) == null) result.put(target, new HashMap<String,Double>());
				result.get(target).put(source, weight+revWeight);
			}
		}
		return result;
	}
	
	/**
	 * @param graph the graph.
	 * @return map from each node names to nodes.
	 */
	public static Map<String,FdNode> makeNodes(Map<String,Map<String,Double>> graph) {
		Map<String,FdNode> result = new HashMap<String,FdNode>();
		for (String nodeName : graph.keySet()) {
            double nodeWeight = 0.0;
            for (double edgeWeight : graph.get(nodeName).values()) {
                nodeWeight += edgeWeight;
            }
			result.put(nodeName, new FdNode(nodeName, nodeWeight));
		}
		return result;
	}
	
    /**
     * Converts a given graph into a list of edges.
     * 
     * @param graph the graph.
     * @param nameToNode map from node names to nodes.
     * @return the given graph as list of edges.
     */
    public static List<FdEdge> makeEdges(Map<String,Map<String,Double>> graph, 
            Map<String,FdNode> nameToNode) {
        List<FdEdge> result = new ArrayList<FdEdge>();
        for (String sourceName : graph.keySet()) {
            for (String targetName : graph.get(sourceName).keySet()) {
                FdNode sourceNode = nameToNode.get(sourceName);
                FdNode targetNode = nameToNode.get(targetName);
                double weight = graph.get(sourceName).get(targetName);
                result.add( new FdEdge(sourceNode, targetNode, weight) );
            }
        }
        return result;
    }
    
    
    /**
     * Calculate a Pseudo-random value for initial position
     * @param counter
     * @param dimension
     * @return
     */
    private static double myRandom(int counter, int dimension) {
    	double RANDRANGE = 0.1;
    	
    	double ret = 0.0;
    	if(dimension == 0) 
    		ret = (double)counter * 0.5921;
    	if(dimension == 1)
    		ret = (double)counter * 0.4129;
    	
    	int tmp = (int)ret;
    	ret -= (double)tmp;
    	
    	ret += ((Math.random() - 0.5) * RANDRANGE);
    	
    	return ret;
    	
    }
    
    
	/**
	 * Returns, for each node in a given list,
	 * a random initial position in two- or three-dimensional space. 
	 * 
	 * @param nodes node list.
     * @param is3d initialize 3 (instead of 2) dimension with random numbers.
	 * @return map from each node to a random initial positions.
	 */
	public static Map<FdNode,double[]> makeInitialPositions(List<FdNode> nodes, boolean is3d) {
        Map<FdNode,double[]> result = new HashMap<FdNode,double[]>();
        int counter = 0;
        for (int i = 0; i < nodes.size(); i++) {
        	FdNode node = nodes.get(i);

			double[] position = null;
			if(initialpos != null && i < initialpos.size()) {
				position = initialpos.get(i);
			}
			else {
				position = new double[]
					{ myRandom(counter, 0) - 0.5,
                    myRandom(counter, 1) - 0.5,
                    is3d ? Math.random() - 0.5 : 0.0 };
				System.out.println("[ph] initial population is too small");
			}
            
            result.put(node, position);
            counter++;
		}
		return result;
	}
	
	/**
	 * Set fixed nodes with their positions
	 * @param nameToNode
	 * @param nodeToPosition
	 * @param fixlist
	 */
	public static void setFixNodes(
			Map<String,FdNode>nameToNode, Map<FdNode,double[]>nodeToPosition, Vector fixlist) {
	
		// if there are no fix node, then return
		if(fixlist == null) return;
		
		// for each fix nodes
		for(int i = 0; i < fixlist.size(); i++) {
			OutputNode on = (OutputNode)fixlist.elementAt(i);
			FdNode node = nameToNode.get(Integer.toString(on.id));
			if(node == null) continue;
			node.isFixed = true;
			double[] pos = nodeToPosition.get(node);
			pos[0] = on.x;
			pos[1] = on.y;
			nodeToPosition.put(node, pos);
		}
		
	}
	
	/**
	 * Writes a given layout and clustering into the specified file.
	 */
	private static void vectorizeNodes(ForceDirectedLayout fdl, Vector nodelist) {
		
		nodelist.clear();
		ArrayList<FDLVertex> layoutVerts = fdl.getVertices();
		for( int i = 0; i < layoutVerts.size(); i++ ){
			FDLVertex v = layoutVerts.get(i);
			OutputNode on = new OutputNode();
			on.id = v.getID();
			on.x = v.getPositionX();
			on.y = v.getPositionY();
			nodelist.add(on);
		}
	}
	
	
	public static void exec(Vector edgelist, Vector nodelist, Vector fixlist) {
//		System.out.println("start Persistent homology guided force-directed layout");
		Graph graph = constructGraph(edgelist, initialpos);

        ForceDirectedLayout fdl = new ForceDirectedLayout(graph, initialpos);
        for(int i = 0; i < 100; i++) {
            fdl.update();
        }
		vectorizeNodes(fdl, nodelist);
	}
}
