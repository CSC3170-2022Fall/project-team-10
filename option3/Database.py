class Database:
    def __init__(self):
        self.tables = [] # a list of class Table

    def do_command(self, command): # command: class Command
        if (command.type == "create table"):
            pass
        elif (command.type == "create table as"):
            pass
        elif (command.type == "load"):
            pass
        elif (command.type == "store"):
            pass
        elif (command.type == "insert"):
            pass
        elif (command.type == "print"):
            pass
        elif ((command.type == "quit") or (command.type == "exit")):
            pass
        elif (command.type == "select"):
            pass
        return

    def create_table():
        pass
    
    def load(self, name): # name: string
        pass
    
    def store(self, name): # name: string
        pass
    
    def insert(self, name): # name: string
        pass
    
    def print(self, name): # name: string
        pass
    
    def quit(self):
        pass
    
    def select(self, column, table, condition): # column: a list names, table: a list of table names, condition: a list of class condition
        pass
