from Database import Database
from Interpreter import interpreter

def main():
    #initialize the database
    database = Database()

    #read from terminal
    quit_flag = 0
    while quit_flag == 0:
        instr = input('> ')
        try:
            cmd = interpreter(instr)    # go to interpreter
            quit_flag = database.do_command(cmd)
        except Exception as error_flag:
            print(error_flag)

main()
