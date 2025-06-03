import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._allNodes = []
        self._allEdges = []
        self._idMapOrdini = {}

    @staticmethod
    def _getAllStores():
        return DAO._getAllStores()

    def _getAllNodes(self):
        return self._grafo.nodes

    def _buildGraph(self, store, k):
        self._grafo = nx.DiGraph()
        self._allNodes = []
        self._allEdges = []
        self._idMapOrdini = {}
        self._allNodes = DAO._getAllNodes(store.store_id)
        for node in self._allNodes:
            self._idMapOrdini[node.order_id] = node
        self._allEdges = DAO._getAllEdges(store.store_id, k)

        for edge in self._allEdges:
            if (source := self._idMapOrdini[edge["source"]]) and (target := self._idMapOrdini[edge["target"]]):
                self._grafo.add_edge(source, target, weight=edge['weight'])
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getLongestPath(self):
        return
