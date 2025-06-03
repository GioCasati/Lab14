from copy import deepcopy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._allNodes = []
        self._allEdges = []
        self._idMapOrdini = {}
        self._heaviestPath = None
        self._highestCost = 0

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

    def _getLongestPath(self, start):
        x = list(nx.bfs_tree(self._grafo, start)) # non ha senso
        x.remove(start)
        return x

    def _getHeaviestPath(self, start):
        self._heaviestPath = None
        self._highestCost = 0
        parziale = [start]
        for node in nx.neighbors(self._grafo, start):
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()
        return self._heaviestPath, self._highestCost

    def _ricorsione(self, parziale):
        if (new_costo := self._costo(parziale)) > self._highestCost:
            self._highestCost = new_costo
            self._heaviestPath = deepcopy(parziale)
        for node in nx.neighbors(self._grafo, prec := parziale[-1]):
            if self._grafo[prec][node]['weight'] < self._grafo[parziale[-2]][prec]['weight']:
                parziale.append(node)
                self._ricorsione(parziale)
                parziale.pop()

    def _costo(self, parziale):
        costo = 0
        for i in range(1, len(parziale)):
            costo += self._grafo[parziale[i - 1]][parziale[i]]['weight']
        return costo