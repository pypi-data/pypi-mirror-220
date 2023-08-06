from typing import Union, TypedDict

from tablate.type.primitives import TextAlignment, BaseDivider


########################################################################################################################
### InputDicts #########################################################################################################
########################################################################################################################


### Grid FrameDict #####################################################################################################

class MinGridInputColumnDict(TypedDict):
    string: Union[str, int, float]

class GridInputColumnDict(MinGridInputColumnDict, total=False):
    width: Union[int, str]
    align: TextAlignment
    divider: BaseDivider

### Table InputDict ####################################################################################################

class MinTableInputColumnDict(TypedDict):
    key: str

class TableInputColumnDict(MinTableInputColumnDict, total=False):
    width: Union[int, str]
    align: TextAlignment
    divider: BaseDivider


# todo: getting into colours / styles de shihou, have two fields... one general, and one which specifies header... if no header included, inherits...
