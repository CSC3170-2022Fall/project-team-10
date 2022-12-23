class Table:    
    #  Possible value for coltype: int(), numeric(,), char(), varchar(), text
    def __init__(self):
        self.name = ""
        self.column = [] # a list of column names
        self.data = [] # a list of string rows
        self.coltype = [] # type of each column
        self.notnull = [] # notnull: 1, default: 0
        self.dflt_value = [] # default value
        self.pk = [] # primary key: 1, default: 0
    
    def join(table): # This part should return a new table by Cartesian product of two table
        table_1 = table[0]
        table_2 = table[1]
        flag_1 = []
        flag_2 = []
        for i in len(table_1.column):
            for j in len(table_2.column):
                if table_1.column[i] == table_2.column[j]:
                    flag_1.append(i)
                    flag_2.append(j)
        if len(flag_1) == 0:
            print("Can not natural join two tables that do not have the same column")
        else:
            new_column = []
            new_data = []
            for item in table_1.column: # Create new column list
                new_column.append(item)
            for item in table_2.column:
                new_column.append(item)
            for i in len(table_1.data):  # Create new data list
                for j in len(table_1.data):
                    for k in len(flag_1):
                        if table_1.data[i][k] == table.data[j][k]: # Determine if the elements are the same
                            data = []
                            data.append[table_1.data[i]]
                            data.append[table_1.data[i]]
                            new_data.append[data]
            for k in len(flag_2): # Delete the same column
                idx = len(table_1.column)+flag_2[k]
                new_column.pop(idx)
                for item in new_data:
                    item.pop(idx)
        return
