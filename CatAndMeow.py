from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


# dot -Tpng CatMeow.dot -o CatMeow.png
# dot -Tpng program.dot -o program.png

variables = {} # dictonary to hold all declared and intialized variables, basically the state


# can declare variables with numbers (value), strings (value_STRING), and boolean (value_BOOLEAN)
def process_variable_declarations(declaration): 
    name = declaration.name # get the name of the variable being declared
    

    if declaration.value: # check if there is value (values are used with expressions)
        
        value = process_expression(declaration.value) # evaluate the value whether it be string or a number
        
        if name in variables: # check if the variable has already been declared
            raise Exception(f"Variable '{name}' declared already") # if variable does not exist
        
    
    
        variables[name] = value # store varaible in dictonary
        
    
    elif declaration.value_STRING:
        value_STRING = declaration.value_STRING
        variables[name] = f'"{value_STRING}"'
        
    elif declaration.value_BOOL is not None: # requires is not None because if only check for declaration.value_BOOL, false would not trigger it

        if declaration.value_BOOL:  # If hungry is true
            value_BOOL = declaration.value_BOOL
            
        else:  # If hungry is false
            value_BOOL = False

    
        value_BOOL = declaration.value_BOOL
        variables[name] = value_BOOL
       
    else: # if varaible is not being intialized, just set it to None
        value = None  # Initialize with None if no value is provided
        
        
        
        


# evaluate assignments after being declared
def process_assignment(assignment):
    
    name = assignment.name # get variable name
    if name not in variables: # check to make sure variable is declared first
        raise Exception(f"Variable '{name}' is not declared.") # raise exception if not been declared
    
    # Evaluate the value and update the variable
    
    if assignment.value:
        variables[name] = process_expression(assignment.value) # evalaute the value, and store in dictonary

    elif assignment.value_STRING: # if the value is a STRING, we dont have to call the expression function
       
        value_STRING = assignment.value_STRING
        variables[name] = f'"{value_STRING}"'
      
        
    elif assignment.value_BOOL is not None: # requires is not None because if only check for declaration.value_BOOL, false would not trigger it

        if assignment.value_BOOL:  # If hungry is true
            value_BOOL = assignment.value_BOOL
            
        else:  # If hungry is false
            value_BOOL = False

       
        value_BOOL = assignment.value_BOOL
        variables[name] = value_BOOL
      
    else: # if varaible is not being intialized, just set it to None
        value = None  # Initialize with None if no value is provided





# process print statements to print 
def process_print_statement(print_statement):
    
    value = print_statement.value # get the value of print object 
    
    if isinstance(value, str): # if it a string, print it
            print(value)
    else:
        result = process_expression(value) # passes the expression or variable through process_expression() and if it is a variable, it will search up the value in the variables dictionary
        print(result)
        
        


    

    
# evalaute the right handside of the equal sign for example "Meow cat = 3 + 7 + (3*8)" or "Meow cat = doggy"
# has issues with telling difference between declared variables strings, assumes it is not declared : "Variable 'DOG' is not declared."
# if it is a type string (whether it be declared variable or actual string), will search in the variables dictonary for the vallue
# only works with numbers, expressions and declared variables, not strings or booleans
def process_expression(expression):
    

    if hasattr(expression, "left"):
        
        # Extract left term
        left_value = process_expression(expression.left)
        
        
        # Extract operators and right terms
        operators = getattr(expression, 'operator')
        rights = getattr(expression, 'right')
        
        
        # Iterate over the attributes operators and right terms, matches operator to the rightside value  
        for operator, right in zip(operators, rights):

            right_value = process_expression(right)
            
            
            if operator == "+": # if operator is addition
                left_value += right_value 
            elif operator == "-": # if operator is subtraction
                left_value -= right_value
            elif operator == "*": # if operator is multiplication
                left_value *= right_value
            elif operator == "/": # if operator is division
                if right_value == 0: 
                    raise Exception("Cannot divide by zero.") # make sure not dividing by zero
                left_value /= right_value
            elif operator == "%": # if operator is modulo
                if right_value == 0:
                    raise Exception("Cannot divide by zero.") # make sure not modulo by zero
                left_value %= right_value
            else:
                raise Exception(f"Operator not allowed: {operator}") # if operator not listed, do not allow
        

    #check if it is an integer
    elif isinstance(expression, int):
        
        return expression
        
    
    
    # check if it is an type string (a declare variable)
    elif isinstance(expression, str):
        
    
        if expression not in variables:
            raise Exception(f"Variable '{expression}' is not declared.")
        value = variables[expression]
        

        # if variable has not been intialized yet
        if value is None:
            raise Exception(f"Variable '{expression}' is declared but not initialized.")
        
        

        # check if the value of the variable and make sure it is a number
        if not isinstance(value, (int, float, str, bool )):
            raise Exception(f"Variable '{expression}' is not a number or a string or boolean.")
        
        return value
        
    else:        
        raise Exception(f"Type not allowed") # if any other than attribute left, then not allowed
    
    return left_value # return the the total value (if operated on, return thhe value after all operations preformed)
  
    

    
    
    
    
    

        
# processes conditions for while loops and if statements
def process_condition(condition):
    
    
    left = process_expression(condition.left) # get evaluated left side of comparator
    # print(left)
    right = process_expression(condition.right) # get evaluated right side of comparator
    # print(right)
    comparator = condition.comparator # get the actual comparator symbol
    
    # evaluate the left and right side
    if comparator == "==":
        return left == right
    elif comparator == "!=":
        return left != right
    elif comparator == "<":
        return left < right
    elif comparator == ">":
        return left > right
    else:
        raise Exception(f"Comparator not allowed: {comparator}")




# evaluate while loops
def process_while_loops(whileloop):
    condition = whileloop.condition # get the while loop condition
    
    while process_condition(condition): # evaluate the while loop condition every loop 
        
        # for each statement in the while loop body, we want to evaluate it 
        for stmt in whileloop.statements:
            # check what type of statement it is 
            if stmt.__class__.__name__ == "VariableDeclaration":
                process_variable_declarations(stmt)
            elif stmt.__class__.__name__ == "Assignment":
                process_assignment(stmt)
            elif stmt.__class__.__name__ == "PrintStatement":
                process_print_statement(stmt)
            elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop_flex(stmt)
            elif stmt.__class__.__name__ == "ForLoop":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "WhileLoop":
                process_while_loops(stmt)
            elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
            else:
                raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")
            

    
    

def process_for_loop(forloop): 
    
    # make copy of orignal intialization value to start loop
    start_value = process_expression(forloop.valueSTART)
    end_value = process_expression(forloop.valueEND)
   
    
    while (start_value  <=  end_value ):
            
        for stmt in forloop.statements:
            # check what type of statement it is 
            if stmt.__class__.__name__ == "VariableDeclaration":
                process_variable_declarations(stmt)
            elif stmt.__class__.__name__ == "Assignment":
                process_assignment(stmt)
            elif stmt.__class__.__name__ == "PrintStatement":
                process_print_statement(stmt)
            elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop_flex(stmt)
            elif stmt.__class__.__name__ == "ForLoop":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "WhileLoop":
                process_while_loops(stmt)
            elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
            else:
                raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")
            
        start_value = start_value + 1 # incrementer
            
            
def process_for_loop_flex(forloop): 
    
    
    #if for loop intialized with variables and you alter the state of the variables, it will affect the execution
    while (process_expression(forloop.valueSTART)  <=  process_expression(forloop.valueEND ) ):
        
        for stmt in forloop.statements:
            # check what type of statement it is 
            if stmt.__class__.__name__ == "VariableDeclaration":
                process_variable_declarations(stmt)
            elif stmt.__class__.__name__ == "Assignment":
                process_assignment(stmt)
            elif stmt.__class__.__name__ == "PrintStatement":
                process_print_statement(stmt)
            elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "ForLoop":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "WhileLoop":
                process_while_loops(stmt)
            elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
            else:
                raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")
            

# evaluate if statements 
def process_if_conditions(ifcondition):
    
    condition = ifcondition.condition # get if condition 
    
    if process_condition(condition): # check if condition to be true, then do 
        
        # evalaute each statement in the true body
        for stmt in ifcondition.statements:
            if stmt.__class__.__name__ == "VariableDeclaration":
                process_variable_declarations(stmt)
            elif stmt.__class__.__name__ == "Assignment":
                process_assignment(stmt)
            elif stmt.__class__.__name__ == "PrintStatement":
                process_print_statement(stmt)
            elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "ForLoop":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "WhileLoop":
                process_while_loops(stmt)
            elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
            else:
                raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")
    
    # if condition was false the else body if there an else boy
    elif hasattr(ifcondition, 'else_statements') :
        # evaluate each statement
        for stmt in ifcondition.else_statements:
            if stmt.__class__.__name__ == "VariableDeclaration":
                process_variable_declarations(stmt)
            elif stmt.__class__.__name__ == "Assignment":
                process_assignment(stmt)
            elif stmt.__class__.__name__ == "PrintStatement":
                process_print_statement(stmt)
            elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "ForLoop":
                process_for_loop(stmt)
            elif stmt.__class__.__name__ == "WhileLoop":
                process_while_loops(stmt)
            elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
            else:
                raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")




        

# inteprets statements in my parse tree
def interpret(program_model):
    
    for stmt in program_model.statements:
        
        # check what type of statement it is and evalaute it
        if stmt.__class__.__name__ == "VariableDeclaration":
            process_variable_declarations(stmt)
        elif stmt.__class__.__name__ == "Assignment":
            process_assignment(stmt)
        elif stmt.__class__.__name__ == "PrintStatement":
            process_print_statement(stmt)
        elif stmt.__class__.__name__ == "ForLoopFLEX":
                process_for_loop_flex(stmt)
        elif stmt.__class__.__name__ == "ForLoop":
            process_for_loop(stmt)
        elif stmt.__class__.__name__ == "WhileLoop":
            process_while_loops(stmt)
        elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)
    
        else:
            raise Exception(f"Statement not allowed: {stmt.__class__.__name__} ")


    

def main(debug=False):
    this_folder = dirname(__file__)
    
    
    CatAndMeow_mm = metamodel_from_file(join(this_folder, 'CatAndMeow.tx'), debug=False) # creates the meta model my programming langauge
    metamodel_export(CatAndMeow_mm, join(this_folder, 'CatMeow.dot')) # create dot file to get image of programming language

    

    program_model = CatAndMeow_mm.model_from_file(join(this_folder, 'program.cat')) # creates parse tree of my program
    model_export(program_model, join(this_folder, 'program.dot')) # creates dot file to get image of programming language
    interpret(program_model) # call the interpreter on my program model, basically the parse tree

    
    
if __name__ == "__main__":
    main(debug=True)
