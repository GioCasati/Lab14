import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._store = None
        self._node = None

    def _fillDDStore(self):
        self._view._ddStore.options = []
        for store in self._model._getAllStores():
            self._view._ddStore.options.append(ft.dropdown.Option(data=store, key=str(store), on_click=self._readDDStore))

    def handleCreaGrafo(self, e):
        self._node = None
        if not self._store:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona uno store!", color="red"))
            self._view.update_page()
            return
        if not (self._view._txtIntK.value.isdigit()):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Immettere un numero intero!", color="red"))
            self._view.update_page()
            return
        n, e = self._model._buildGraph(self._store, int(self._view._txtIntK.value))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {n} nodi e {e} archi"))

        # riempi dd partenza
        self._view._ddNode.options.clear()
        for node in self._model._getAllNodes():
            self._view._ddNode.options.append(ft.dropdown.Option(data=node, key=str(node), on_click=self._readDDNode))
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        if not self._node:
            self._view.txt_result.controls.append(ft.Text("Seleziona un nodo di partenza!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Percorso più lungo che parte da {self._node}:"))
        for node in self._model._getLongestPath(self._node):
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def handleRicorsione(self, e):
        self._view.txt_result.controls.clear()
        if not self._node:
            self._view.txt_result.controls.append(ft.Text("Seleziona un nodo di partenza!", color="red"))
            self._view.update_page()
            return
        nodes, cost = self._model._getHeaviestPath(self._node)
        self._view.txt_result.controls.append(ft.Text(f"Percorso di peso maggiore che parte da {self._node}, con costo {cost}"))
        for node in nodes:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def _readDDStore(self, e):
        self._store = e.control.data

    def _readDDNode(self, e):
        self._node = e.control.data