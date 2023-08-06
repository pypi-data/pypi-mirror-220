
__version__ = (0, 3, 1)
__author__ = 'Carlos Gaete-Morales'


from .arrays import *
from .arrays import _from_feather, _from_csv  # Require by symbolx
from .utils import union_multi_coords  # Require by symbolx
from .setting import settings