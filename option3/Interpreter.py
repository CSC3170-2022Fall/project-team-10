from Condition import Condition
from Command import Command

def inputSplit(instr):
    ind = instr.find(';')
    if ind == -1:
        raise Exception('SQL syntax error: require \';\' for the end of the statement')
    commandstr = instr[:ind]
    commandstr = commandstr.replace('\n', ' ')
    commandstr = commandstr.replace('\t', ' ')
    commandsp = commandstr.split(' ')
    commandl = []
    for i in commandsp:
        if i != '':
            commandl.append(i)
    return commandl, commandstr
        
def typeDectect(command):
    if len(command) >= 4 and command[0] == 'create' and command[1] == 'table' and command[3] == 'as':
        return 'create table as'
    elif len(command) >= 2 and command[0] == 'create' and command[1] == 'table':
        return 'create table'
    elif command[0] == 'load':
        return 'load'
    elif command[0] == 'store':
        return 'store'
    elif len(command) >= 2 and command[0] == 'insert' and command[1] == 'into':
        return 'insert into'
    elif command[0] == 'print':
        return 'print'
    elif command[0] == 'select':
        return 'select'
    elif command[0] == 'quit':
        return 'quit'
    elif command[0] == 'exit':
        return 'exit'
    else:
        raise Exception('SQL syntax error: unknown command type')
    
def create_table_interpreter(commandl):
    thiscommand = Command()
    thiscommand.type = 'create table'
    if len(commandl) < 3:
        raise Exception('SQL syntax error: create table command lacks table name')
    thiscommand.name.append(commandl[2])
    if len(commandl) < 4:
        raise Exception('SQL syntax error: create table command lacks column name')
    columnlist = commandl[3:]
    if columnlist[0][0] != '(' or columnlist[-1][-1] != ')':
        raise Exception('SQL syntax error: create table command requires parentheses')
    columns = []
    for i in columnlist:
        if i != '(' and i != ')' and i != '()': 
            column = i
            column = column.replace('(', '')
            column = column.replace(')', '')
            ind = column.find(',')
            if ind != -1:
                l = column.split(',')
                for j in l:
                    if j != '':
                        columns.append(j)
            else:
                if column in columns:
                    raise Exception('SQL syntax error: create table command has duplicate columns')
                columns.append(column)
    if len(columns) < 1:
        raise Exception('SQL syntax error: create table command lacks columns')
    for i in columns:
        thiscommand.column.append(i)
    return thiscommand

def load_interpreter(commandl):
    thiscommand = Command()
    thiscommand.type = 'load'
    if len(commandl) < 2:
        raise Exception('SQL syntax error: load command lacks table name')
    elif len(commandl) > 2:
        raise Exception('SQL syntax error: load command has meaningless parameter')
    thiscommand.name.append(commandl[1])
    return thiscommand
    
def store_interpreter(commandl):
    thiscommand = Command()
    thiscommand.type = 'store'
    if len(commandl) < 2:
        raise Exception('SQL syntax error: store command lacks table name')
    elif len(commandl) > 2:
        raise Exception('SQL syntax error: store command has meaningless parameter')
    thiscommand.name.append(commandl[1])
    return thiscommand 

def insert_into_interpreter(commandl, commands):
    thiscommand = Command()
    thiscommand.type = 'insert into'
    if len(commandl) < 3:
        raise Exception('SQL syntax error: insert command lacks table name')
    thiscommand.name.append(commandl[2])
    if len(commandl) < 4 or commandl[3] != 'values':
        raise Exception('SQL syntax error: insert command lacks key word values')
    values = commands.split('values ')[1]
    quoindlist = []
    commaindlist = []
    for i in range(len(values)):
        if values[i] == "'":
            quoindlist.append(i)
        if values[i] == ',':
            commaindlist.append(i)
    if len(quoindlist) % 2 != 0:
        raise Exception("SQL syntax error: lack completed ''")
    for i in range(0, len(quoindlist), 2):
        n = []
        for j in commaindlist:
            if j > quoindlist[i + 1] or j < quoindlist[i]:
                n.append(j)
        if len(n) != 0:
            commaindlist = n
    valuelist = []
    if len(commaindlist) < 1 :
        values = values.lstrip()
        values = values.rstrip()
        valuelist.append(values)
    else:
        for i in range(len(commaindlist)):
            onevalue = ''
            if i == 0:
                onevalue = values[:commaindlist[i]]
            else:
                onevalue = values[commaindlist[i-1]+1:commaindlist[i]]
            onevalue = onevalue.lstrip()
            onevalue = onevalue.rstrip()
            valuelist.append(onevalue)
        onevalue = values[commaindlist[-1] + 1:]
        onevalue = onevalue.lstrip()
        onevalue = onevalue.rstrip()
        valuelist.append(onevalue)
    if len(valuelist) < 1:
        raise Exception('SQL syntax error: insert command lacks rows')
    for i in valuelist:
        thiscommand.rows.append(i)
    return thiscommand
    
def print_interpreter(commandl):
    thiscommand = Command()
    thiscommand.type = 'print'
    if len(commandl) < 2:
        raise Exception('SQL syntax error: print command lacks table name')
    elif len(commandl) > 2:
        raise Exception('SQL syntax error: print command has meaningless parameter')
    thiscommand.name.append(commandl[1])
    return thiscommand 

def deal_condition(cond):
    thiscondition = Condition()
    optl = ['>', '>=', '==', '<', '<=', '!=']
    for opt in optl:
        if cond.find(opt) != -1:
            if opt == '>' and cond.find('>=') != -1:
                continue
            if opt == '<' and cond.find('<=') != -1:
                continue
            thiscondition.relation = opt
            condl = cond.split(opt)
            if len(condl) != 2:
                raise Exception('SQL syntax error: illegal comapring expression')
            left = condl[0]
            left = left.lstrip()
            left = left.rstrip()
            thiscondition.left = left
            if left[0] =="'" and left[-1] =="'":
                thiscondition.left_type = 'string'
            elif left.replace('.', '').isdigit():
                thiscondition.left_type = 'number'
            else:
                thiscondition.left_type = 'column'
            right = condl[1]
            right = right.lstrip()
            right = right.rstrip()
            thiscondition.right = right
            if right[0] =="'" and right[-1] =="'":
                thiscondition.right_type = 'string'
            elif right.replace('.', '').isdigit():
                thiscondition.right_type = 'number'
            else:
                thiscondition.right_type = 'column'
            return thiscondition
    raise Exception('SQL syntax error: no such comparing operation')
            
                
            

def select_interpreter(commandl, commands):
    thiscommand = Command()
    thiscommand.type = 'select'
    if 'from' not in commandl:
        raise Exception('SQL syntax error: select command lacks from key word')
    fromindex = commandl.index('from')
    if fromindex == 1:
        raise Exception('SQL syntax error: select command lacks column parameter')
    whereindex = len(commandl)
    for i in range(len(commandl)):
        if commandl[i] == 'where':
            whereindex = commandl.index('where')
            break
    if fromindex + 1 == whereindex:
        raise Exception('SQL syntax error: select command lacks table name parameter')
    for i in range(1, fromindex):
        fnl = commandl[i].split(',')
        for n in fnl:
            if n != '':
                fn = n.lstrip()
                fn = fn.rstrip()
                thiscommand.column.append(fn)
    if len(thiscommand.column) < 1:
        raise Exception('SQL syntax error: select command lacks column parameter')
    for i in range(fromindex + 1, whereindex):
        cnl = commandl[i].split(',')
        for n in cnl:
            if n != '':
                cn = n.lstrip()
                cn = cn.rstrip()
                thiscommand.name.append(cn)
    if len(thiscommand.name) < 1:
        raise Exception('SQL syntax error: select command lacks table name parameter')
    
    if whereindex < len(commandl):
        if whereindex == len(commandl) -1:
            raise Exception('SQL syntax error: select command lacks conditions parameter')
        conditionstring = commands.split(' where ')[1]
        if len(commands.split(' where ')) > 2:
            raise Exception('SQL syntax error: select command has duplicate key word where')
        conditionlist = conditionstring.split(' and ')
        for i in range(len(conditionlist)):
            conditionlist[i] = conditionlist[i].lstrip()
            conditionlist[i] = conditionlist[i].rstrip()
        for cond in conditionlist:
            thiscommand.condition.append(deal_condition(cond))
    return thiscommand


def create_table_as_interpreter(commandl, commands):
    thiscommand = Command()
    thiscommand.type = 'create table as'
    if len(commandl) < 3:
        raise Exception('SQL syntax error: create table as command lacks table name')
    thiscommand.name.append(commandl[2])
    if commandl[4] != 'select':
        raise Exception('SQL syntax error: create table as command lacks key world select')
    commandl = commandl[4:]
    commands = commands[commands.find('select'):]
    if 'from' not in commandl:
        raise Exception('SQL syntax error: select command lacks from key word')
    fromindex = commandl.index('from')
    if fromindex == 1:
        raise Exception('SQL syntax error: select command lacks column parameter')
    whereindex = len(commandl)
    for i in range(len(commandl)):
        if commandl[i] == 'where':
            whereindex = commandl.index('where')
            break
    if fromindex + 1 == whereindex:
        raise Exception('SQL syntax error: select command lacks table name parameter')
    for i in range(1, fromindex):
        fnl = commandl[i].split(',')
        for n in fnl:
            if n != '':
                fn = n.lstrip()
                fn = fn.rstrip()
                thiscommand.column.append(fn)
    if len(thiscommand.column) < 1:
        raise Exception('SQL syntax error: select command lacks column parameter')
    for i in range(fromindex + 1, whereindex):
        cnl = commandl[i].split(',')
        for n in cnl:
            if n != '':
                cn = n.lstrip()
                cn = cn.rstrip()
                thiscommand.name.append(cn)
    if len(thiscommand.name) < 1:
        raise Exception('SQL syntax error: select command lacks table name parameter')
        
    if whereindex < len(commandl):
        if whereindex == len(commandl) -1:
            raise Exception('SQL syntax error: select command lacks conditions parameter')
        conditionstring = commands.split(' where ')[1]
        if len(commands.split(' where ')) > 2:
            raise Exception('SQL syntax error: select command has duplicate key word where')
        conditionlist = conditionstring.split(' and ')
        for i in range(len(conditionlist)):
            conditionlist[i] = conditionlist[i].lstrip()
            conditionlist[i] = conditionlist[i].rstrip()
        for cond in conditionlist:
            thiscommand.condition.append(deal_condition(cond))
    return thiscommand


def interpreter(instr):
    try:
        commandl, commands = inputSplit(instr)
        t = typeDectect(commandl)
        if t == 'create table':
            return create_table_interpreter(commandl)
        elif t == 'create table as':
            return create_table_as_interpreter(commandl, commands)
        elif t == 'load':
            return load_interpreter(commandl)
        elif t == 'store':
            return store_interpreter(commandl)
        elif t == 'insert into':
            return insert_into_interpreter(commandl, commands)
        elif t == 'print':
            return print_interpreter(commandl)
        elif t == 'select':
            return select_interpreter(commandl, commands)
        elif t == 'quit' or t == 'exit':
            com = Command()
            com.type = t
            return com
        else:
            raise Exception('SQL syntax error: no such SQL command')
    except:
        raise Exception('error: SQL syntax error')
        
           
        
# instr = input('>')
# acommand = interpreter(instr)
# print(acommand.type)
# print(acommand.name)
# print(acommand.column)
# print(acommand.rows)
# for thiscondition in acommand.condition:
#     print(thiscondition.left)
#     print(thiscondition.left_type)
#     print(thiscondition.relation)
#     print(thiscondition.right)
#     print(thiscondition.right_type)  


