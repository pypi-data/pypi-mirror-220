from .libloader import G_LIB
import os
from ezoognn.utils.properties_utils import Properties

MAXINT = 2147483647
INVALID_INT = -2147483648


def get_ezoo_home(cfg_file=None) -> str:
    if cfg_file is not None:
        properties = Properties(cfg_file).get_properties()
        return properties['gnn.home']
    else:
        return str(os.getenv('GNN_HOME')) if os.getenv('GNN_HOME') else '/tmp/ezoodb/gnn'
        # return os.path.join(os.path.expanduser('~'), '.ezoo')
