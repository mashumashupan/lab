import glob
import re
import sys
from collections import defaultdict

from graph import Cluster, Edge, Graph, Node
from graphParser import GraphParser


class RelayPoints:
    def __init__(self, id, edge_id, x, y):
        self.id = id
        self.edge_id = edge_id
        self.x = x
        self.y = y


class edgeBundledGraphParser(GraphParser):
    def __init__(self, path):
        super().__init__(path)
        self.cluster_dict = defaultdict(set)

    def get_cluster_info(self, start):
        """
        :returns: the dict of Cluster (key: node_id, value: cluster_id)
        """
        cluster_data = self.data[start:]
        for i in range(0, len(cluster_data), 2):
            cluster_id, x, y, r = cluster_data[i][0:4]
            children = cluster_data[i + 1][1:]

            cluster = Cluster(cluster_id, x, y, r, children)
            self.clusters.add(cluster)

            for node_id in children:
                self.cluster_dict[int(node_id)] = int(cluster_id)

    def get_bundled_edge_info(self, start, end):
        """
        :returns: the set of Edge(including bundled edges)
        """

        print(len(self.nodes))
        relay_point_id = len(self.nodes)
        checked_edges = defaultdict(set)

        for i in range(0, len(self.data[start:end]), 2):
            edge_info = self.data[start:end][i]

            # check node1 and node2
            node1, node2 = int(edge_info[1]), int(edge_info[2])
            n1, n2 = min(node1, node2), max(node1, node2)
            if n2 in checked_edges[n1]:
                # already added the edge
                continue

            else:
                checked_edges[n1].add(n2)

                # coodinates = [edge_id, x0, y0, ..., x10, y10]
                coodinates = list(map(float, self.data[start:end][i + 1]))

                relay_points = []
                for i in range(1, len(coodinates), 2):
                    edge_id, x, y = coodinates[0], coodinates[i], coodinates[i + 1]
                    rp = RelayPoints(relay_point_id, edge_id, x, y)
                    relay_point_id += 1
                    relay_points.append(rp)

                bundled_edge = Edge(*edge_info, relay_points=relay_points)
                self.edges.add(bundled_edge)

    def gen_graph(self):
        """
        :returns Graph:
        """

        ## get node info
        node_title_raw = 0
        if self.data[node_title_raw][0] == "#nodes":
            NODE_NUM = int(self.data[node_title_raw][1])
            node_raw_start = node_title_raw + 1
        else:
            raise Exception("Wrong FileTemplate: NODE_NUM not found")

        self.get_node_info(node_raw_start, node_raw_start + NODE_NUM)

        ## get edge info
        edge_title_raw = node_raw_start + NODE_NUM
        if self.data[edge_title_raw][0] == "#edges":
            EDGE_NUM = int(self.data[edge_title_raw][1])
            edge_raw_start = edge_title_raw + 1

        else:
            raise Exception("Wrong FileTemplate: EDGE_NUM not found")

        self.get_bundled_edge_info(edge_raw_start, edge_raw_start + (EDGE_NUM * 2))

        ## get cluster info
        cluster_title_raw = edge_raw_start + (EDGE_NUM * 2)
        if self.data[cluster_title_raw][0] == "#clusters":
            CLUSTER_NUM = int(self.data[cluster_title_raw][1])
            cluster_raw_start = cluster_title_raw + 1
        else:
            print(self.data[cluster_title_raw:])
            raise Exception("Wrong FileTemplate: CLUSTER_NUM not found")

        self.get_cluster_info(cluster_raw_start)

        # elif self.data[edge_title_raw][0] == "#clusters":
        #     print()
        #     self.get_bundled_edge_info(edge_raw_start, edge_raw_start + (EDGE_NUM * 2))

        #     ## get cluster info
        #     cluster_title_raw = edge_raw_start + (EDGE_NUM * 2)
        #     CLUSTER_NUM = int(self.data[cluster_title_raw][1])
        #     cluster_raw_start = cluster_title_raw + 1
        #     self.get_cluster_info(cluster_raw_start)

        # else:
        #     raise Exception("Wrong FileTemplate: EDGE_NUM or CLUSTER_NUM not found")

        return Graph(self.nodes, self.edges, self.clusters)

    def export_cluster_dict(self):
        return self.cluster_dict


if __name__ == "__main__":
    args = sys.argv

    # 一括変換
    if len(args) == 1:
        # path = "./result/bundled/layout0-1.csv"
        # html_path = "test.html"
        # _parser = edgeBundledGraphParser(path)
        # graph = _parser.gen_graph()
        # cluster_dict = _parser.export_cluster_dict()

        # graph.to_html(html_path, is_bundled=True, cluster_dict=cluster_dict)

        csv_files = glob.glob("./result/bundled/*")

        for path in csv_files:
            # get file name
            ma = re.search(r"layout([0-9]+)-([0-9]+)\.csv", path)
            if ma is None:
                print("Wrong File Path", fname)
                continue

            # parse csv data
            fname = "layout{0}-{1}.html".format(ma.group(1), ma.group(2))
            html_path = "./result/bundled_html_files_no_edges_inside/" + fname

            _parser = edgeBundledGraphParser(path)
            graph = _parser.gen_graph()
            cluster_dict = _parser.export_cluster_dict()

            graph.to_html(html_path, is_bundled=True, cluster_dict=cluster_dict)

            print("Done: ", fname)

    elif len(args) == 2:
        # デバッグ用: 1つのcsvファイルを実行
        path = args[1]

        # parse csv data
        _parser = edgeBundledGraphParser(path)
        graph = _parser.gen_graph()
        cluster_dict = _parser.export_cluster_dict()

        html_path = "./test.html"
        graph.to_html(html_path, is_bundled=True, cluster_dict=cluster_dict)

        print("Done")

    else:
        raise Exception("WrongArgs")
