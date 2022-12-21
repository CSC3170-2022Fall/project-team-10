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
    
    def join(table_1,table_2): # This part should return a new table by Cartesian product of two table
        if len(table_1.data) != len(table_2.data):
            print("Can not do join two tables of different lengths")
        else:
            new_column = []
            new_data = []
            for i in len(table_1.column):
                new_column.append(table_1.column[i])
            for j in len(table_2.column):
                new_column.append(table_2.column[j])
            for i in len(table_1.data):
                for j in len(table_2.data):
                    data = table_1.data[i] + table_2.data[j]
                    new_data.append(data)
        return new_column, new_data
