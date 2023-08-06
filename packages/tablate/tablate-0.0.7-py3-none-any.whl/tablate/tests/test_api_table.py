from tablate import Table
from tablate.classes.bases.TablateSet import TablateSet
from tablate.tests.test_objs import column_list1, row_list1

new_table1 = Table(column_list1, row_list1)
new_table2 = Table(column_list1, row_list1)

new_table1.print()

new_set = TablateSet([new_table1, new_table2])
print("###")
new_set.print()

newer_set = TablateSet([new_set])