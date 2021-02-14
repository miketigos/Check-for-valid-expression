# File: statement-eval.py
# Author: michael thomas
# Date: 8/25/2020
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements

from pathlib import Path
import sys

import re  # For regular expressions
class BadLine(Exception):
    pass

def interpret_statements(filename):

    # open file and create a list to hold each lines tokens
    f = open_file(filename)
    variables = {}
    index = 0
    
    for line in f:
        line_no_comment = line[:line.find('#')].strip()
        line_tokens = line_no_comment.split()

        index += 1
        
        if len(line_tokens) == 0:
            continue
        else:
            try:
                if not is_valid_line(line_tokens):
                    raise BadLine
                value = interpret_one_statement(line_tokens, variables)
                print("Line {}: {} = {}".format(index, line_tokens[0], value))
            except BadLine:
                print("Line {}: Invalid Statement".format(index))    
 
def interpret_one_statement(tokens, variables):

    if not is_valid_line(tokens):
        raise BadLine
    value = get_token_value(tokens[2], variables)
    i = 3
    while i < len(tokens):
        if tokens[i] == '+':
            value += get_token_value(tokens[i+1], variables)
        elif tokens[i] == '-':
            value -= get_token_value(tokens[i+1], variables)  
        else:
            raise BadLine
        i += 2
    variables[tokens[0]] = value
    return value              

def open_file(filename):
    try:
        f = open(filename, 'r')
        return f
    except OSError:
        print("Directory/File Not found") 
        sys.exit()
        
def is_valid_line(line): 
    if len(line) == 0: 
        return False # check for empty string
    if re.fullmatch(r'[a-zA-Z_]\w*', line[0]) == None:
        return False #check for invalid variable name
    if line[1] != '=':
        return False
    if len(line) % 2 == 0:
        return False        
    return True  

def get_token_value(token, variables):
    try:
        value = float(token)
        return value
    except ValueError:
        if token in variables:
            return variables[token]
        else:
            raise BadLine            

if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)

