class Command:
    type = "" #possibile values: 'create table' 'create table as' 'load' 'store' 'insert into' 'print' 'quit' 'exit' 'select'
    name = [] # a list for name of tables, all elements are in form of string
    # e.g. ['student', 'instructor']
    #for load commamd it is <name>, only one element
    #for create table, create table as, store, insert into and print command, it is <table name>, only one element
    #for select command, it is <table name> after "for", may be more than one
    # if the command is create table as, then the first element is used for <table name> after create table, the rest is used for <table name> in <select clause>
    rows = [] #used for insert command, refers to <literal>, in form of string even the original data is number
    # e.g. if the column of the table is ['instructor_id', 'salary', 'instructor_name']
    # then one instance may be ['123', '12000.00', 'Tom']
    column = [] # a list of string that store the column name, in form of string
    # used for select and create command, refers to <column name>
    #e.g. ['studemt_id', 'student_name', 'major']
    condition = [] # a list of condition classes
    #used for select command <condition caluse>
    #the logical relationship between conditions is "and"
    