from typing import Union

from tablate.api.Tablate import Tablate

from tablate.api.modules.Text import Text
from tablate.api.modules.Grid import Grid
from tablate.api.modules.Table import Table
from tablate.classes.bases.TablateSet import TablateSet

TablateUnion = Union[Tablate, Text, Grid, Table, TablateSet]