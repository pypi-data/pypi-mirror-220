from __future__ import annotations

from importlib.metadata import version

from tablate.api.Tablate import Tablate
from tablate.api.modules.Grid import Grid
from tablate.api.modules.Table import Table
from tablate.api.modules.Text import Text

from tablate.api.functions import concat

try:
    __version__ = version('tablate')
except ModuleNotFoundError:
    pass
