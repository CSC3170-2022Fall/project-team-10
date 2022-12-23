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
    
    def join(self,table): # This part should return a new table by Cartesian product of two table
        table_1 = self
        table_2 = table
        flag_1 = []
        flag_2 = []
        new_table = Table()
        for i in range(len(table_1.column)):
            new_table.column.append(table_1.column[i])
            new_table.coltype.append(table_1.coltype[i])
            new_table.notnull.append(table_1.notnull[i])
            new_table.dflt_value.append(table_1.dflt_value[i])
            new_table.pk.append(table_1.pk[i])            
        for i in range(len(table_2.column)):
            new_table.column.append(table_2.column[i])
            new_table.coltype.append(table_2.coltype[i])
            new_table.notnull.append(table_2.notnull[i])
            new_table.dflt_value.append(table_2.dflt_value[i])
            new_table.pk.append(table_2.pk[i])            


        for i in range(len(table_1.column)):
            for j in range(len(table_2.column)):
                if table_1.column[i] == table_2.column[j]:
                    flag_1.append(i)
                    flag_2.append(j)


        if len(flag_1) == 0:
            # Outer Join
            for i in range(len(table_1.data)):
                for j in range(len(table_2.data)):
                    new_data = table_1[i]+table_2[j]
                    new_table.data.append(new_data)
            return new_table

        else:
            # Natural Join
            for i in len(table_1.data):  
                for j in len(table_2.data): 
                    for k in len(flag_1):
                        if table_1.data[i][flag_1[k]] == table_2.data[j][flag_2[k]]: # Determine if the elements are the
                            new_data = table_1[i]+table_2[j]
                            new_table.data.append(new_data)
            return new_table
