from typing import Literal, TypedDict, Union, Optional, List, Dict


########################################################################################################################
### Literals ###########################################################################################################
########################################################################################################################

TextAlignment = Literal["left", "center", "right"]
HeaderAlignment = Literal["column", "center"]

BaseBorder = Literal["none", "blank", "thin", "thick", "double"]
HeaderColumnDivider = Literal["rows", "blank", "thin", "thick", "double"]
RowColumnDivider = Literal["blank", "thin", "thick", "double"]

########################################################################################################################
### FrameDicts #########################################################################################################
########################################################################################################################

### Text FrameDict #####################################################################################################

class TextBoxColumnDict(TypedDict):
    width: Union[int, str]
    divider: RowColumnDivider

class TextFrameDict(TypedDict):
    type: Literal["string"]
    column_list: List[TextBoxColumnDict]
    string: str
    base_divider: BaseBorder
    max_lines: Optional[int]
    align: TextAlignment
    padding: int
    trunc_value: str


### Grid FrameDict #####################################################################################################


class GridColumnFrameDict(TypedDict):
    width: Union[int, str]
    divider: RowColumnDivider
    string: str
    align: TextAlignment
    padding: int
    trunc_value: str

class GridFrameDict(TypedDict):
    type: Literal["grid"]
    column_list: List[GridColumnFrameDict]
    base_divider: BaseBorder
    max_lines: Optional[int]


### Table FrameDict ####################################################################################################

class TableColumnFrameDict(TypedDict):
    width: Union[int, str]
    divider: RowColumnDivider
    key: str
    align: TextAlignment
    padding: int
    trunc_value: str

class TableRowsFrameDict(TypedDict):
    type: Literal["table"]
    column_list: List[TableColumnFrameDict]
    table_row_list: List[Dict[str, Union[str, int, float]]]
    row_line_divider: BaseBorder
    base_divider: BaseBorder


########################################################################################################################
### InputDicts #########################################################################################################
########################################################################################################################

### Grid FrameDict #####################################################################################################

class MinGridInputColumnDict(TypedDict):
    string: Union[str, int, float]

class GridInputColumnDict(MinGridInputColumnDict, total=False):
    width: Union[int, str]
    align: TextAlignment
    divider: RowColumnDivider

### Table InputDict ####################################################################################################

class MinTableInputColumnDict(TypedDict):
    key: str

class TableInputColumnDict(MinTableInputColumnDict, total=False):
    width: Union[int, str]
    align: TextAlignment
    divider: RowColumnDivider

