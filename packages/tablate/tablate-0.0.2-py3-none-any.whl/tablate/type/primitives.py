from typing import Literal

TextAlignment = Literal["left", "center", "right"]
HeaderAlignment = Literal["column", "center"]

Border = Literal["blank", "thin", "thick", "double"]
BaseDivider = Literal["none", "blank", "thin", "thick", "double"]
ColumnDivider = Literal["blank", "thin", "thick", "double"]
HeaderColumnDivider = Literal["rows", "blank", "thin", "thick", "double"]

HtmlTextNode = Literal["th", "td"]