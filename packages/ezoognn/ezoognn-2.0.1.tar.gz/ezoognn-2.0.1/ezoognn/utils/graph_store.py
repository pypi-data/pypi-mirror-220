from ..ezoo_graph import EzooGraph
from ..ezoocall import HandlerGenerateType
from typing import Optional


class GraphStore:
    _instance = None
    _inited = False

    def __init__(self, url=None, cfg_file=None):
        """
        Graph store, stores the graph name and EzooGraph's mapping dict.
        """
        if not GraphStore._inited:
            GraphStore._inited = True
            self.store = {}
        self.url = url
        self.cfg_file = cfg_file

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_singleton_directly(cls):
        return cls._instance

    def reset(self):
        if self.store != None:
            for g_obj in self.store.values():
                g_obj.close_graph()
            self.store.clear()

    def store_graph(self, g_name, e_graph):
        self.store[g_name] = e_graph

    def remove_graph(self, g_name):
        if g_name in self.store:
            self.store[g_name].close_graph()
            del self.store[g_name]

    def get_graph(self, g_name, gdi_ptr=0, restore_file="", restore_url="", schema_path="", iconf_path="",
                  cache_edge=True, cache_node=True, init_type=HandlerGenerateType.Load, src_db="",
                  del_props={}, add_props={}) -> Optional[EzooGraph]:
        if g_name in self.store:
            return self.store.get(g_name)
        else:
            e_graph = None
            try:
                e_graph = EzooGraph(url=self.url, dbname=g_name, cfg_file=self.cfg_file, gdi_ptr=gdi_ptr,
                                    restore_file=restore_file, restore_url=restore_url, schema_path=schema_path,
                                    iconf_path=iconf_path, cache_edge=cache_edge, cache_node=cache_node, init_type=init_type,
                                    src_db=src_db, del_props=del_props, add_props=add_props)
                self.store[g_name] = e_graph
            except Exception as e:
                self.client = None
                print(f"{str(e)}")
            return e_graph
