from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


# dot -Tpng CatMeow.dot -o CatMeow.png

variables = {} # dictonary to hold all declared and intialized variables, basically the state


def process_variable_declarations(declaration): 
    name = declaration.name # get the name of the variable being declared
    

    if declaration.value: # check if there is value
        value = process_expression(declaration.value) # evaluate the value whether it be string or a number
        
        if name in variables: # check if the variable has already been declared
            raise Exception(f"Variable '{name}' declared already") # if variable does not exist
        
    else: # if varaible is not being intialized, just set it to None
        value = None  # Initialize with None if no value is provided
    
    variables[name] = value # store varaible in dictonary
   

    


# evaluate assignments after being declared
def process_assignment(assignment):
    
    name = assignment.name # get variable name
    if name not in variables: # check to make sure variable is declared first
        raise Exception(f"Variable '{name}' is not declared.") # raise exception if not been declared
    
    # Evaluate the value and update the variable
    variables[name] = process_expression(assignment.value) # evalaute the value, and store in dictonary

# process print statements to print 
def process_print_statement(print_statement):
    
    value = print_statement.value # get the value of print object 

    if isinstance(value, str): # if it a string, print it
            print(value)
    else:
        result = process_expression(value) # if it is not a string, evaluate the expression or get value from variable dictionary 
        print(result)


    

    
# evalaute the right handside of the equal sign for example "Meow cat = 3 + 7 + (3*8)" or "Meow cat = doggy"
def process_expression(expression):
    #check if it is an integer
    if isinstance(expression, int):
         
        return expression
    
    
    # check if it is an string 
    elif isinstance(expression, str):
        
    
            if expression not in variables:
                raise Exception(f"Variable '{expression}' is not declared.")
            value = variables[expression]

            # if variable has not been intialized yet
            if value is None:
                raise Exception(f"Variable '{expression}' is declared but not initialized.")

            # check if the value of the variable and make sure it is a number
            if not isinstance(value, (int, float)):
                raise Exception(f"Variable '{expression}' is not a number.")
            
            return value
        
    
    
    elif hasattr(expression, "left"):
        
        
        
        # Extract left term
        left_value = process_expression(expression.left)
        
        
        # Extract operators and right terms
        operators = getattr(expression, 'operator')
        rights = getattr(expression, 'right')
        
      
        # Iterate over the attributes operators and right terms
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
        
        return left_value

    else:        
        raise Exception(f"Type not allowed") # if any other than attribute left, then not allowed
    
  
    



        
# processes conditions for while loops and if statements
def process_condition(condition):
    left = process_expression(condition.left) # get evaluated left side of comparator
    right = process_expression(condition.right) # get evaluated right side of comparator
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
        elif stmt.__class__.__name__ == "WhileLoop":
            process_while_loops(stmt)
        elif stmt.__class__.__name__ == "IfCondition":
                process_if_conditions(stmt)

            

        else:
            raise Exception(f"Statement not allowed: {stmt.__class__.__name__}")


    

def main(debug=False):
    this_folder = dirname(__file__)
    
    
    CatAndMeow_mm = metamodel_from_file(join(this_folder, 'CatAndMeow.tx'), debug=False) # creates the meta model my programming langauge
    metamodel_export(CatAndMeow_mm, join(this_folder, 'CatMeow.dot')) # create dot file to get image of programming language

    

    program_model = CatAndMeow_mm.model_from_file(join(this_folder, 'program.cat')) # creates parse tree of my program
    model_export(program_model, join(this_folder, 'program.dot')) # creates dot file to get image of programming language
    interpret(program_model) # call the interpreter on my program model, basically the parse tree

    
    
if __name__ == "__main__":
    main(debug=True)
