class Table:    
    def __init__(self):
        self.name = ""
        self.column = [] # a list of column names
        self.data = [] # a list of string rows
    
    def join(self,table): # This part should return a new table by Cartesian product of two table
        table_1 = self
        table_2 = table
        flag_1 = []
        flag_2 = []
        new_table = Table()
        for i in range(len(table_1.column)):
            new_table.column.append(table_1.column[i])         
        for i in range(len(table_2.column)):
            new_table.column.append(table_2.column[i])            


        for i in range(len(table_1.column)):
            for j in range(len(table_2.column)):
                if table_1.column[i] == table_2.column[j]:
                    flag_1.append(i)
                    flag_2.append(j)

        if len(flag_1) == 0:
            # Outer Join
            for i in range(len(table_1.data)):
                for j in range(len(table_2.data)):
                    new_data = table_1.data[i]+table_2.data[j]
                    new_table.data.append(new_data)
            return new_table

        else:
            # Natural Join
            for i in range(len(table_1.data)): 
                t1_data = table_1.data[i] 
                for j in range(len(table_2.data)):
                    t2_data = table_2.data[j] 
                    for k in range(len(flag_1)):
                        if t1_data[flag_1[k]] == t2_data[flag_2[k]]: # Determine if the elements are the
                            new_data = t1_data+t2_data
                            new_table.data.append(new_data)
            # print(new_table.column)
            # for i in range(len(new_table.data)):
            #     print(new_table.data[i])
            return new_table
