import os
from Table import Table

class Database:
    def __init__(self):
        self.tables = [] # a list of class Table

    def do_command(self, command): # command: class Command
        if (command.type == "create table"):
            self.create_table(command.name[0], command.column)
        elif (command.type == "create table as"):
            selected  = self.select(command.column, command.name[1:], command.condition)
            self.create_table(command.name[0], selected)
        elif (command.type == "load"):
            self.load(command.name[0])
        elif (command.type == "store"):
            self.store(command.name[0])
        elif (command.type == "insert into"):
            self.insert(command.name[0], command.rows)
        elif (command.type == "print"):
            self.print(command.name[0])
        elif ((command.type == "quit") or (command.type == "exit")):
            return -1
        elif (command.type == "select"):
            self.select(command.column,command.name,command.condition)
        return 0

    def create_table(self, table_name, column_name):
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables.pop(i)
                break
        table = Table()
        table.name = table_name
        for name in column_name:
            table.column.append(name)
        self.tables.append(table)
        return

    def create_table_as(self, table_name, selected):
        for i in range(len(self.tables)):
            if self.tables[i].name == table_name:
                self.tables.pop(i)
                break
        table = selected
        table.name = table_name
        self.tables.append(table)
        return
   
    # Return 0 for normally terminates, return -1 for terminates with error
    def load(self, table_name): # file_name: string
        # Get table names from file
        if (not os.path.exists(table_name + ".db")):
            print("Error: File doesn't exist.")
            return -1
        new_table = Table()
        new_table.name = table_name
        with open(table_name + ".db", "r") as file:
            col_row = True
            for line in file:
                if (line[-1] == "\n"):
                    line = line[:-1]
                line_list = line.split(",")
                # Read column name
                if (col_row == True):
                    new_table.column = line_list
                    col_row = False
                # Read data
                else:
                    for i in range(len(line_list)):
                        try:
                            line_list[i] = eval(line_list[i])
                        except:
                            pass
                    new_table.data.append(line_list)
        self.tables.append(new_table)
        print("Loaded " + table_name + ".db")
        return 0

    # Return 0 for normally terminates, return -1 for terminates with error
    def store(self, table_name): # table_name: string
        # Find corresponding Table object
        flag = -1
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                flag = 0
                break
        if (flag == -1):
            print("Error: Table doesn't exist.")
            return -1
        with open(table_name + ".db", "w") as file:
            # Write column name
            for i in range(len(table.column)):
                if (i != 0):
                    file.write(",")
                file.write(table.column[i])
            file.write("\n")
            # Write data
            for i in range(len(table.data)):
                for j in range(len(table.data[i])):
                    if (j != 0):
                        file.write(",")
                    file.write(str(table.data[i][j]))
                if (i != len(table.data) - 1):
                    file.write("\n")
        print("Stored " + table_name + ".db")
        return 0

    # Return 0 for normally terminates, return -1 for terminates with error
    def insert(self, table_name, literal): # name: string, literal: string tuple
        # Find corresponding Table object
        flag = -1
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                flag = 0
                break
        if (flag == -1):
            print("Error: Table doesn't exist.")
            return -1
        if (len(literal) < len(table.column)):
            print("Error: Lack literals.")
            return -1
        elif (len(literal) > len(table.column)):
            print("Error: Too many literals.")
            return -1
        for i in range(len(literal)):
            try:
                literal[i] = eval(literal[i])
            except:
                if ((literal[i][0] == "\"") or (literal[i][0] == "\'")):
                    literal[i] = literal[i][1:]
                if ((literal[i][-1] == "\"") or (literal[i][0] == "\'")):
                    literal[i] = literal[i][:-1]
        for i in range(len(table.data)):
            # Check the uniqueness of data
            for j in range(len(table.column)):
                flag_ = 0
                if (table.data[i][j] != literal[j]):
                    flag_ = 1
                    break
            if (flag_ == 0):
                return 0
        table.data.append(literal)
        return 0

    def print(self, table_name): # name: string
        # Find corresponding Table object
        flag = -1
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                flag = 0
                break
        if (flag == -1):
            print("Error: Table doesn't exist.")
            return -1
        pformat = ""
        # Find proper length for each column
        for i in range(len(table.column)):
            max_len = len(table.column[i])
            for j in range(len(table.data)):
                if (len(str(table.data[j][i])) > max_len):
                    max_len = len(str(table.data[j][i]))
            pformat += "%-"
            pformat += str(max_len + 2)
            pformat += "s"
        # Print column name
        print(pformat % tuple(map(str, table.column)))
        # Print data
        for i in range(len(table.data)):
            print(pformat % tuple(map(str, table.data[i])))
        return 0
    
    def __satis(self,value_test,value_cond,relation):
        if relation == '=' and value_test == value_cond:
            return True
        if relation == '>=' and value_test >= value_cond:
            return True
        if relation == '<=' and value_test <= value_cond:
            return True
        if relation == '<' and value_test < value_cond:
            return True
        if relation == '>' and value_test > value_cond:
            return True
        return False
    
    def select(self, column, table, condition): # column: a list names, table: a list of table names, condition: a list of class condition
        # 单table select
        ori_table = Table()                     # ori_table 是进入condition时的原数据
        new_table = Table()                     # new_table 是输出的结果table
        # 单表select 构建单表的
        if len(table) == 1:                     # 此处table为select输出的参数，参数内容是一个包含所要调用的table的name的list  
            for i in range(len(self.tables)):
                if self.tables[i].name == table[0]:
                    ori_table = self.tables[i]
                    break
        elif len(table) == 2:
            flag_tb1 = 0
            flag_tb2 = 0
            table0 = Table()
            table1 = Table()
            for i in range(len(self.tables)):
                if self.tables[i].name == table[0]:
                    table0 = self.tables[i]
                    flag_tb1 = 1
                    break

            for j in range(len(self.tables)):
                if self.tables[j].name == table[1]:
                    table1 = self.tables[j]
                    # print('students的type:',type(table0))
                    # print('students.data的type:',type(table0.data))
                    ori_table = table0.join(table1)
                    # print('finish natural join')
                    flag_tb2 = 1
                    break
            if flag_tb1 == 0 and flag_tb2 == 0:
                print("This database doesn\'t have such two table.")
                return
            if flag_tb1 == 0:
                print("This database doesn\'t have such table named:%s"%table[0])
                return
            if flag_tb2 == 0:
                print("This database doesn\'t have such table named:%s"%table[1])
                return

        else:
            if len(table) == 0:
                print("This command needs at least 1 table")
            else:
                print('Error: More than 2 tables')
            return
        #############################################################################################################


        # 更新new_table的columns
        ind = []                                    # index列表：记录的是我们所需要的column在ori_table中的index
        for k in range(len(column)):
            for j in range(len(ori_table.column)):
                if column[k] == ori_table.column[j]:
                    new_table.column.append(ori_table.column[j])
                    ind.append(j)
        # print('初始化新表column长度',len(new_table.column))
        # print('finish new table')

        # 根据condition选数据
        # 单条件
        if len(condition) == 1:
            # print("单条件")
            flag_condi = 0
            col_ind = 0                         # col_ind: condition中left所需column在ori_table中的index
            cond = condition[0]
            for j in range(len(ori_table.column)):
                if ori_table.column[j] == cond.left:
                    flag_condi = 1
                    col_ind = j
                    # 判断condition中的数据类型是否符合table中，若不符合则报错
                    if cond.right_type == 'string' and type(ori_table.data[0][j]) != str:
                        # print('string')
                        # print(type(ori_table.data[0][j]))
                        print("Error: The left and right data types of condition \"%s\" do not match. "%cond.left)
                        return
                    elif cond.right_type ==  'number':
                        if cond.right.find('.') != -1:
                            # print(cond.right)
                            if type(ori_table.data[0][j]) != float:
                                # print('float')
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond.left)
                                return   
                        else: 
                            if type(ori_table.data[0][j]) != int:
                                # print(type(ori_table.data[0][j]))
                                # print('int')
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond.left)
                                return         
            if flag_condi == 0:              
                print("The condition's column cannot be found in table.")
                return 

            ori_data = ori_table.data     # ori_data: ori_table中data的全集
            if cond.right_type != 'column':
                for id in range(len(ori_data)):
                    test_data = ori_data[id] 
                    cond_value = cond.right         # ID == 12009 
                    test_value = test_data[col_ind]
                    if cond.right_type ==  'number':
                        if cond_value.find('.')!= -1:
                            cond_value = float(cond_value)
                        else:
                            cond_value = int(cond_value)
                    elif cond.right_type == 'string':
                        test_value == str(test_value)
                
                    test_relation = cond.relation
                    if self.__satis(test_value,cond_value,test_relation): 
                        # print('enter')
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data)

            else:
                condition_id = 0
                condition_col = cond.right
                for i in range(len(ori_table.column)):
                    if ori_table.column[i] == condition_col:
                        condition_id = i
                        break
                for id in range(len(ori_data)):
                    test_data = ori_data[id] 
                    if test_data[col_ind] == test_data[condition_id]:
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data)   

        # 双条件
        elif len(condition) == 2:
            # print("单条件")
            flag_1 = 0
            flag_2 = 0
            col_ind_1 = 0
            col_ind_2 = 0
            cond_1 = condition[0]
            cond_2 = condition[1]
            for j in range(len(ori_table.column)):
                if ori_table.column[j] == cond_1.left:
                    flag_1 += 1
                    col_ind_1 = j
                    if cond_1.right_type == 'string' and type(ori_table.data[0][j]) != str:
                        print("Error: The left and right data types of condition \"%s\" do not match"%cond_1.left)
                        return   
                    elif cond_1.right_type ==  'number':
                        if cond_1.right.find('.')!= -1:
                            if type(ori_table.data[0][j]) != float:
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond_1.left)
                                return   
                        else: 
                            if type(ori_table.data[0][j]) != int:
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond_1.left)
                                return                        

            for j in range(len(ori_table.column)):
                if ori_table.column[j] == cond_2.left:
                    flag_2 += 1
                    col_ind_2 = j
                    if cond_2.right_type == 'string' and type(ori_table.data[0][j] )!= str:
                        print("Error: The left and right data types of condition \"%s\" do not match"%cond_2.left)
                        return   
                    elif cond_2.right_type ==  'number':
                        if cond_2.right.find('.')!= -1:
                            if type(ori_table.data[0][j]) != float:
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond_2.left)
                                return   
                        else: 
                            if type(ori_table.data[0][j]) != int:
                                print("Error: The left and right data types of condition \"%s\" do not match"%cond_2.left)
                                return         

            if flag_1 == 0 or flag_2 == 0:
                print("The condition's column cannot be found in table.")
                return 

            ori_data = ori_table.data
            if cond_1.right_type != 'column' and cond_2.right_type != 'column':
                for id in range(len(ori_data)):
                    test_data = ori_data[id]
                    cond_value_1 = cond_1.right
                    test_value_1 = test_data[col_ind_1]
                    if cond_1.right_type ==  'number':
                        if cond_value_1.find('.')!= -1:
                            cond_value_1 = float(cond_value_1)
                        else:
                            cond_value_1 = int(cond_value_1)
                    elif cond_1.right_type == 'string':
                        test_value_1 == str(test_value_1)
                    
                    cond_value_2 = cond_2.right
                    test_value_2 = test_data[col_ind_2]
                    if cond_2.right_type ==  'number':
                        if cond_value_2.find('.')!= -1:
                            cond_value_2 = float(cond_value_2)
                        else:
                            cond_value_2 = int(cond_value_2)
                    elif cond_2.right_type == 'string':
                        test_value_2 == str(test_value_2)

                    test_relation_1 = cond_1.relation
                    test_relation_2 = cond_2.relation
                    if self.__satis(test_value_1,cond_value_1,test_relation_1) and self.__satis(test_value_2,cond_value_2,test_relation_2):
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data)

            elif cond_1.right_type == 'column' and cond_2.right_type != 'column':
                condition_id = 0
                condition_col = cond_1.right
                for i in range(len(ori_table.column)):
                    if ori_table.column[i] == condition_col:
                        condition_id = i
                        break                
                for id in range(len(ori_data)):
                    test_data = ori_data[id] 
                    cond_value_2 = cond_2.right
                    test_value_2 = test_data[col_ind_2]
                    test_relation_2 = cond_2.relation
                    if cond_2.right_type ==  'number':
                        if cond_value_2.find('.')!= -1:
                            cond_value_2 = float(cond_value_2)
                        else:
                            cond_value_2 = int(cond_value_2)
                    elif cond_2.right_type == 'string':
                        test_value_2 == str(test_value_2)
                    
                    if test_data[col_ind_1] == test_data[condition_id] and self.__satis(test_value_2,cond_value_2,test_relation_2) :
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data) 

            elif cond_2.right_type == 'column' and cond_1.right_type != 'column':
                condition_id = 0
                condition_col = cond_2.right
                for i in range(len(ori_table.column)):
                    if ori_table.column[i] == condition_col:
                        condition_id = i
                        break    

                for id in range(len(ori_data)):
                    test_data = ori_data[id]
                    cond_value_1 = cond_1.right
                    test_value_1 = test_data[col_ind_1]
                    test_relation_1 = cond_1.relation
                    if cond_1.right_type ==  'number':
                        if cond_value_1.find('.')!= -1:
                            cond_value_1 = float(cond_value_1)
                        else:
                            cond_value_1 = int(cond_value_1)
                    elif cond_1.right_type == 'string':
                        test_value_1 == str(test_value_1)

                    test_data = ori_data[id] 
                    if test_data[col_ind_2] == test_data[condition_id] and self.__satis(test_value_1,cond_value_1,test_relation_1) :
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data)     

            else: 
                condition_id_1 = 0
                condition_id_2 = 0
                condition_col_1 = cond_1.right
                condition_col_2 = cond_2.right
                flag = 0
                for i in range(len(ori_table.column)):
                    if flag == 2:
                        break
                    if ori_table.column[i] == condition_col_1:
                        condition_id_1 = i
                        flag += 1
                        continue
                    if ori_table.column[i] == condition_col_2:
                        condition_id_2 = i
                        flag += 1
                        continue
                
                for id in range(len(ori_table.data)):
                    test_data = ori_table.data[id]
                    if test_data[condition_id_1] == test_data[cond_1] and test_data[condition_id_2] == test_data[cond_2]:
                        new_data = []
                        for idx in ind:
                            new_data.append(test_data[idx])
                        new_table.data.append(new_data)     
                           
        elif len(condition) >= 3:
            print("Error: # of conditions is more than 2.")
            return 
        else:                       # 无condition情况
            for k in range(len(ori_table.data)):
                new_data = []
                test_data = ori_table.data[k]
                for idx in ind:
                    new_data.append(test_data[idx])
                new_table.data.append(new_data)
            
        # show the data
        print('Select Results:')
        # print('新表column长度: ',len(new_table.column))
        # print('Original data',ori_table.data[0][5],type(ori_table.data[0][5]))
        for k in range(len(new_table.column)):
            print(new_table.column[k],end='\t')
        print()
        if len(new_table.data) == 0:
            print("The result is NONE.")
        else:
            # print('新表数据列长度: ',len(new_table.data))
            for i in range(len(new_table.data)):
                show_data = new_table.data[i] 
                for j in range(len(new_table.column)):
                    print(show_data[j],end='\t')
                print()
        print()
        return new_table

