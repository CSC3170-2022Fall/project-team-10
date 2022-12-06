class Condition:
    left = ""
    left_type = "" # 'int'/ 'float' / 'string' / 'column'
    relation = "" # > < >= <= == !=
    right = ""
    right_type = ""
    
#e.g if the condition is student_name == 'Tom'
# left = "student_name"
# left_type = "column" 
# relation = "==" 
# right = "Tom"
# right_type = "string"

#e.g if the condition is instructor_salary > '12000.00'
# left = "instructor_salary"
# left_type = "column" 
# relation = ">" 
# right = "12000.00"
# right_type = "float"

#e.g if the condition is instructor_salary > '12000'
# left = "instructor_salary"
# left_type = "column" 
# relation = ">" 
# right = "12000"
# right_type = "int"

#The python data type of "left" and "right" is string, but their actual data type is stored in "left_type" and "right_type"