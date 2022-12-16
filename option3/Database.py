import sqlite3
from Table import Table

<<<<<<< HEAD
    def create_table():
        return

    def load(name): # name: string
    
    def store(name): # name: string
        
    def insert(name): # name: string
        
    def print(name): # name: string
    
    def quit():
    
    def select(column, table, condition): # column: a list names, table: a list of table names, condition: a list of class condition
        # return a table needed
        
        return 
=======
class Database:
    def __init__(self):
        self.tables = [] # a list of class Table

    def do_command(self, command): # command: class Command
        if (command.type == "create table"):
            pass
        elif (command.type == "create table as"):
            pass
        elif (command.type == "load"):
            self.load(command.name[0])
        elif (command.type == "store"):
            self.store(command.name[0])
        elif (command.type == "insert into"):
            self.insert(command.name[0], command.rows)
        elif (command.type == "print"):
            self.print(command.name[0])
        elif ((command.type == "quit") or (command.type == "exit")):
            self.quit()
        elif (command.type == "select"):
            pass
        return

    def create_table(self):
        pass
    
    def load(self, file_name): # file_name: string
        # Get table names from file
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
        return

    def store(self, table_name): # table_name: string
        conn = sqlite3.connect(table_name + ".db")
        cursor = conn.cursor
        # Find corresponding Table object
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                break
        # Drop old table if it exists
        cursor.execute("drop table if exists %s" %table_name)
        # Create new table
        pk = []  # Store primary key
        create_sql = "create table %s (" %table_name
        for i in range(len(table.column)):
            create_sql += table.column[i]
            create_sql += " "
            create_sql += table.coltype[i]
            if (table.notnull[i] != 0):
                create_sql += " not null"
            create_sql += " default "
            create_sql += table.dflt_value[i]
            if (table.pk[i] == 1):
                pk.append(table.column[i])
            create_sql += ", "
        create_sql += "primary key "
        create_sql += str(tuple(pk))
        create_sql += ")"
        cursor.execute(create_sql)
        # Insert data to the table
        for i in range(len(table.data)):
            insert_sql = "insert into %s values " %table_name
            insert_sql += str(table.data[i])
            cursor.execute(insert_sql)
        conn.commit()
        conn.close()
        return

    # Return 0 for normally terminates, return -1 for terminates with error
    def insert(self, table_name, literal): # name: string, literal: string tuple
        # Find corresponding Table object
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                break
        for i in range(len(literal)):
            l = literal[i]
            # Check whether the data has proper type
            if (table.coltype[i][0] == "i"):  # Integer
                if (not isinstance(eval(l), int)):
                    print("Error: The type of No." + str(i + 1) + " data should be integer instead of others." )
                    return -1
                literal[i] = eval(l)
            elif (table.coltype[i][0] == "f"):  # Float
                if (not isinstance(eval(l), float)):
                    print("Error: The type of No." + str(i + 1) + " data should be float instead of others." )
                    return -1
                # Check the length of float
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
                n = int(table.coltype[i].split("(")[1].split(")")[0])
                if (n < len(l)):
                    print("Error: No." + str(i + 1) + " data has too many digits")
                    return -1
            elif (table.coltype[i][0] == "v"):  # Varchar
                n = int(table.coltype[i].split("(")[1].split(")")[0])
                if (n < len(l)):
                    print("Error: No." + str(i + 1) + " data has too many digits")
                    return -1
            elif (table.coltype[i][0] == "t"):  # Text
                pass
        # Check the uniqueness of primary key
        for i in range(len(table.data)):
            for j in range(len(table.column)):
                flag = 0
                if ((table.pk[j] == 1) and (table.data[i][j] != literal[j])):
                    flag = 1
            if (flag == 0):
                print("Error: The primary key exists.")
                return -1
        table.data.append(literal)
        return 0

    def print(self, table_name): # name: string
        # Find corresponding Table object
        for i in range(len(self.tables)):
            if (self.tables[i].name == table_name):
                table = self.tables[i]
                break
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
        print(pformat % list(map(str, table.column)))
        # Print data
        for i in range(len(table.data)):
            print(pformat % list(map(str, table.data[i])))
        return
    
    def quit(self):
        pass
    
    def select(self, column, table, condition): # column: a list names, table: a list of table names, condition: a list of class condition
        pass

>>>>>>> refs/remotes/origin/main
