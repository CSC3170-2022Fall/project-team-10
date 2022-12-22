import os
import sqlite3
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
            pass
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
    def load(self, file_name): # file_name: string
        # Get table names from file
        if (not os.path.exists(file_name + ".db")):
            print("Error: File doesn't exist.")
            return -1
        conn = sqlite3.connect(file_name + ".db")
        cursor = conn.cursor()
        cursor.execute("select name from sqlite_master where type = 'table'")
        table_name = cursor.fetchall()
        for i in range(len(table_name)):
            # Check whether the table has been created
            flag = 0
            for j in range(len(self.tables)):
                if (self.tables[j].name == table_name[i][0]):
                    print("Error: Table " + table_name[i][0] + " has been created.")
                    flag = 1
                    break
            # Load file
            if (flag == 0):
                new_table = Table()
                new_table.name = table_name[i][0]
                cursor.execute("PRAGMA table_info('%s')" %table_name[i][0])
                column_attr = cursor.fetchall()
                for j in range(len(column_attr)):
                    new_table.column.append(column_attr[j][1])
                    new_table.coltype.append(column_attr[j][2].lower())
                    new_table.notnull.append(column_attr[j][3])
                    new_table.dflt_value.append(column_attr[j][4])
                    new_table.pk.append(column_attr[j][5])
                cursor.execute("select * from %s" %table_name[i][0])
                datas = cursor.fetchall()
                for j in datas:
                    new_table.data.append(list(j))
                self.tables.append(new_table)
        conn.close()
        return 0

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
        conn = sqlite3.connect(table_name + ".db")
        cursor = conn.cursor()
        # Drop old table if it exists
        cursor.execute("drop table if exists %s" %table_name)
        # Create new table
        pk = []  # Store primary key
        create_sql = "create table %s (" %table_name
        for i in range(len(table.column)):
            create_sql += table.column[i]
            create_sql += " "
            if (table.coltype != []):
                create_sql += table.coltype[i]
            if (table.notnull != []):
                if (table.notnull[i] != 0):
                    create_sql += " not null"
            if (table.dflt_value != []):
                if (table.dflt_value[i] != None):
                    create_sql += " default "
                    create_sql += table.dflt_value[i]
            if (table.pk != []):
                if (table.pk[i] == 1):
                    pk.append(table.column[i])
            if (i != len(table.column) - 1):
                create_sql += ", "
        if (pk != []):
            create_sql += ", "
            create_sql += "primary key "
            create_sql += str(tuple(pk))
        create_sql += ")"
        cursor.execute(create_sql)
        # Insert data to the table
        for i in range(len(table.data)):
            insert_sql = "insert into %s values " %table_name
            insert_sql += str(tuple(table.data[i]))
            cursor.execute(insert_sql)
        conn.commit()
        conn.close()
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
        if (len(literal) != len(table.column)):
            print("Error: Lack literals.")
            return -1
        for i in range(len(literal)):
            l = literal[i]
            # Check whether the data has proper type
            if (table.coltype != []):
                if (table.coltype[i][0] == "i"):  # Integer
                    if (not isinstance(eval(l), int)):
                        print("Error: The type of No." + str(i + 1) + " data should be integer instead of others." )
                        return -1
                    literal[i] = eval(l)
                elif (table.coltype[i][0] == "d"):  # Decimal
                    if ((not isinstance(eval(l), float)) and (not isinstance(eval(l), int))):
                        print("Error: The type of No." + str(i + 1) + " data should be decimal instead of others." )
                        return -1
                    # Check the length of decimal
                    m = int(table.coltype[i].split(",")[0].split("(")[1])
                    d = int(table.coltype[i].split(",")[1].split(")")[0])
                    if ("." in l):
                        if (d < len(l.split(".")[1])):
                            print("Error: No." + str(i + 1) + " data has too many decimal digits")
                            return -1
                        if (m < len(l) - 1):
                            print("Error: No." + str(i + 1) + " data has too many digits")
                            return -1
                    else:
                        if (m < len(l)):
                            print("Error: No." + str(i + 1) + " data has too many digits")
                            return -1
                    literal[i] = eval(l)
                elif (table.coltype[i][0] == "c"):  # Char
                    if ((literal[i][0] != '"') or (literal[i][-1] != '"')):
                        print("Error: The type of No." + str(i + 1) + " data should be char instead of others." )
                        return -1
                    literal[i] = literal[i][1: -1]
                    n = int(table.coltype[i].split("(")[1].split(")")[0])
                    if (n < len(l)):
                        print("Error: No." + str(i + 1) + " data has too many digits")
                        return -1
                elif (table.coltype[i][0] == "v"):  # Varchar
                    if ((literal[i][0] != '"') or (literal[i][-1] != '"')):
                        print("Error: The type of No." + str(i + 1) + " data should be varchar instead of others." )
                        return -1
                    literal[i] = literal[i][1: -1]
                    n = int(table.coltype[i].split("(")[1].split(")")[0])
                    if (n < len(l)):
                        print("Error: No." + str(i + 1) + " data has too many digits")
                        return -1
                elif (table.coltype[i][0] == "t"):  # Text
                    if ((literal[i][0] != '"') or (literal[i][-1] != '"')):
                        print("Error: The type of No." + str(i + 1) + " data should be text instead of others." )
                        return -1
                    literal[i] = literal[i][1: -1]
        for i in range(len(table.data)):
            # Check the uniqueness of data
            for j in range(len(table.column)):
                flag_ = 0
                if (table.data[i][j] != literal[j]):
                    flag_ = 1
                    break
            if (flag_ == 0):
                return 0
            # Check the uniqueness of primary key
            flag = 2
            for j in range(len(table.column)):
                if (table.pk != []):
                    if (table.pk[j] == 1):
                        flag = 0
                        if (table.data[i][j] != literal[j]):
                            flag = 1
                            break
            if (flag == 0):
                print("Error: The primary key exists.")
                return -1
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
    
    def select(self, column, table, condition): # column: a list names, table: a list of table names, condition: a list of class condition
        # condition的样例
        #e.g if the condition is student_name == 'Tom'
        # left = "student_name"
        # left_type = "column" 
        # relation = "==" 
        # right = "Tom"
        # right_type = "string"

        # table 的属性：
        # self.name = ""
        # self.column = [] # a list of column names
        # self.data = [] # a list of string rows
        # self.coltype = [] # type of each column
        # self.notnull = [] # notnull: 1, default: 0
        # self.dflt_value = [] # default value
        # self.pk = [] # primary key: 1, default: 0
        
        ''' 
        1. new_table 根据column和condition连接的新表
        2. ori_table 数据库中的原表
        3. result_table 返回的结果无名表
        4. ind[] 原表中所需的column的index
        '''
        # 单table select
        if len(table) == 1:
            new_table = Table()
            for i in range(len(self.tables)):
                if self.tables[i].name == table[0]:
                    ori_table = self.tables[i]
                    break
            # 更新new_table的columns
            ind = []
            for k in range(len(column)):
                for j in range(len(ori_table.column)):
                    if column[k] == ori_table.column[j]:
                        new_table.column.append(ori_table.column[j])
                        new_table.coltype.append(ori_table.coltype[j])
                        new_table.notnull.append(ori_table.notnull[j])
                        new_table.dflt_value.append(ori_table.dflt_value[j])
                        new_table.pk.append(ori_table.pk[j])


            # 根据condition选数据
            if len(condition) != 0:
                for j in range(len(ori_table.column)):
                    if ori_table.column[j] == condition.left:
                        if ori_table.coltype != condition.right_type:
                            print("Error: The left and right data types of condi do not match")
                            return
                        for id in range(len(ori_table.data)):
                            data = ori_table.data[id]
                            if condition.relation == "==" and str(data[j]) == condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue
                            
                            if condition.relation == "<=" and str(data[j]) <= condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue

                            if condition.relation == ">=" and str(data[j]) >= condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue                               

                            if condition.relation == "<" and str(data[j]) < condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue           

                            if condition.relation == ">" and str(data[j]) > condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue            

                            if condition.relation == "!=" and str(data[j]) != condition.right:
                                new_data = []
                                for idx in ind:
                                    new_data.append(data[idx])
                                continue
                        return new_table
            else:
                new_data = []
                for idx in ind:
                    new_data.append(data[idx])
                return new_table


                                

        # 多table select
        else:
