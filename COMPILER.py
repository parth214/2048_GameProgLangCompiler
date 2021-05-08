from sly import Lexer
from sly import Parser
from GAME import *
import sys

 
class GameLexer(Lexer):
    tokens = {NAME, NUMBER, OPERATOR, DIRECTION, ASSIGN, TO, VAR, IS, VALUE, IN,FLOAT, MY_KEYWORDS}
    # tokens = {NUMBER, OPERATOR, DIRECTION, TO, NAME}
 
    ignore = '\t '
 
    literals = {'.', ','}
 
    # Define tokens
    OPERATOR = r"\bADD\b|\bSUBTRACT\b|\bMULTIPLY\b|\bDIVIDE\b"
    FLOAT=r'[+-]?[0-9]+\.[0-9]+'
    DIRECTION = r"\bLEFT\b|\bUP\b|\bRIGHT\b|\bDOWN\b"
    TO = r"TO"
    ASSIGN = r"ASSIGN"
    VAR = r"VAR"
    IS = r"IS"
    VALUE = r"VALUE"
    IN = r"IN"
    NAME = r'[a-zA-Z_][a-zA-Z_]*'
    
    #NEGATIVE=r'-[0-9*'
    MY_KEYWORDS=r"\bADD\b|\bSUBTRACT\b|\bMULTIPLY\b|\bDIVIDE\bMULTIPLY|\bLEFT\b|\bUP\b|\bRIGHT\b|\bDOWN\b|\bTO\b|\bASSIGN\b|\bVAR\b|\bIS\b|\bVALUE\b|\bIN\b"
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
 
    def error(self, t):
        self.index += len(t.value)
        
class GameParser(Parser):
    tokens = GameLexer.tokens
    @_('')
    def statement(self, p):
        pass
    
    @_('FLOAT')
    def statement(self, p):
        print("You have used a FLOAT. Please use proper numbers and commands")

    @_('OPERATOR DIRECTION "."')
    def statement(self, p):
        return ("operator", p.OPERATOR, p.DIRECTION)

    @_('OPERATOR DIRECTION')
    def statement(self, p):
        print("Missing Fullstop for the MOVE Command")
        sys.stderr.write("-1")
        sys.stderr.write("\n")

    @_('ASSIGN FLOAT TO NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Error. You have used a FLOAT in the ASSIGN statement")
        sys.stderr.write("-1")
        sys.stderr.write("\n")

    @_('VALUE IN NUMBER "," NUMBER "."')
    def statement(self, p):
        return ("value", [p.NUMBER0, p.NUMBER1])

    @_('VALUE IN NUMBER "," NUMBER')
    def statement(self, p):
        print("Missing Fullstop for the QUEURY Command")
        sys.stderr.write("-1")
        sys.stderr.write("\n")
 
    @_('ASSIGN NUMBER TO NUMBER "," NUMBER "."')
    def statement(self, p):
        return ("assign", p.NUMBER0, [p.NUMBER1, p.NUMBER2])
 
    @_('VAR NAME IS NUMBER "," NUMBER "."')
    def statement(self, p):
        return ("var", p.NAME, [p.NUMBER0, p.NUMBER1])
 

    @_('ASSIGN NUMBER TO NUMBER "," NUMBER')
    def statement(self, p):        
        print("Missing Fullstop for the ASSIGNMENT Command")
        sys.stderr.write("-1")
        sys.stderr.write("\n")

    @_('VAR NAME IS NUMBER "," NUMBER')
    def statement(self, p):
        print("Missing Fullstop for the NAMING Command")
        sys.stderr.write("-1")
        sys.stderr.write("\n")

    @_('VAR MY_KEYWORDS IS NUMBER "," NUMBER')
    def statement(self, p):
        print("Error. A KEYWORD cant be a variable name")
        sys.stderr.write("-1")
        sys.stderr.write("\n")

    def error(self, p):
        print("Syntax error")
        self.restart()
        sys.stderr.write("-1")
        sys.stderr.write("\n")
        return
 
def after_operation(grid,variableName):
    random_tile_generator(grid)
    printGrid(grid)
    printGridStderr(grid, variableName)

class RUN_GAME:
 
    def __init__(self, tree, grid, variableName,myset):
        self.grid = grid
        self.variableName = variableName
        self.myset=myset
        if tree is None:
            return
        result = self.walkTree(tree)
 
    def walkTree(self, node):
        numbers=[1,4] 
        if node is None:
            return None
 
        elif node[0] == 'operator':
            if(check_it(node[2],self.grid)==1 and all_filled(self.grid)):   
                 print('Game is over. Use assign statement to create possibilities')
            elif (check_it(node[2],self.grid)==2 and all_filled(self.grid)):
                print('operation is a deadend. Try another possible operation')
            else:
                processOperation(node[1], node[2], self.grid, self.variableName,self.myset)
                after_operation(self.grid,self.variableName)
            # printGrid(self.variableName)
 
        elif node[0] == 'assign':
            if node[2][0] < numbers[0] or node[2][0] > numbers[1] or node[2][1]  < numbers[0] or node[2][1] > numbers[1]:
                print("Please enter valid co-ordinates in assign statement.")
                sys.stderr.write("-1")
                sys.stderr.write("\n")
            else:
                x=node[2][0]-1
                y=node[2][1]-1
                self.grid[x][y] = node[1]
                if node[1] == 0:
                    #print("checkpoint  1")
                    my_var_names=self.variableName[x][y]
                    #print(self.variableName[node[2]-1][node[3]-1])
                    splitted=my_var_names.split(",")
                    if splitted!=[]:
                        for i in splitted:
                            #print('checkpoint 2')
                            if i in myset:
                                myset.remove(i)
                            print("reached here")
                    self.variableName[x][y] = ""
                printGrid(self.grid)
                printGridStderr(self.grid, self.variableName)
 
        elif node[0] == 'value':
            if node[1][0] < numbers[0] or node[1][0] > numbers[1] or node[1][1]  < numbers[0] or node[1][1] > numbers[1]:
                print("Please enter valid co-ordinates in query statement.")
                sys.stderr.write("-1")
                sys.stderr.write("\n")
            else:
                x=node[1][0]-1
                y=node[1][1]-1
                if grid[x][y] > 0:
                    print("Value in " + str(node[1][0]) + "," + str(node[1][1]) + " is " + str(grid[x][y]))
                else:
                    print(str(node[1][0]) + "," + str(node[1][1]) + " is empty")
                printGridStderr(self.grid, self.variableName)

 
        elif node[0] == 'var':
            x=node[2][0]-1
            y=node[2][1]-1
            if node[2][0] > (numbers[0]-1) and node[2][0] < (numbers[1]+1) and node[2][1] > (numbers[0]-1) and node[2][1] < (numbers[1]+1) and self.grid[x][y] != 0:
                if (str(node[1]) in myset):
                    print("This variable name already exists. Please choose another variable name.")
                    sys.stderr.write("-1")
                    sys.stderr.write("\n")
                else:
                    myset.add(str(node[1]))
                    if self.variableName[x][y] == "":
                        self.variableName[x][y] += str(node[1])
                    else:
                        self.variableName[x][y] += ","+str(node[1])
                printGridStderr(self.grid, self.variableName)

            elif node[2][0] > (numbers[0]-1) and node[2][0] < (numbers[1]+1) and node[2][1] > (numbers[0]-1) and node[2][1] < (numbers[1]+1) and self.grid[x][y] == 0:
                print("Empty tile can't be named")
                sys.stderr.write("-1")
                sys.stderr.write("\n")                
            else:
                print("Please enter valid co-ordinates while assigning variables.")
                sys.stderr.write("-1")
                sys.stderr.write("\n")
 
        else:
            print("Illegal Command")
            sys.stderr.write("-1")
            sys.stderr.write("\n")
 


def check_it(direction,grid):
    type=""
    flag_vertical=check_vertical(grid)
    flag_horizontal=check_horizontal(grid)


    if(direction=="UP" or direction=="DOWN"):
        if((flag_vertical==False) and (flag_horizontal==False)):
            return 1
        elif((flag_vertical==False) and flag_horizontal):
            return 2
    else:
        if((flag_vertical==False) and (flag_horizontal==False)):
            return 1
        elif((flag_horizontal==False) and flag_vertical):
            return 2
    return 0

def check_vertical(grid):
    flag=False
    for col in range(4):
        for row in range(3):
            if(grid[row][col]==grid[row+1][col]):
                flag=True
                break
    return flag

def check_horizontal(grid):
    flag=False
    for row in range(4):
        for col in range(3):
            if(grid[row][col]==grid[row][col+1]):
                flag=True
                break
    return flag

if __name__ == '__main__':
    lexer = GameLexer()
    parser = GameParser()
    grid = [[0] * 4 for _ in range(4)]
    myset=set()
    variableName = [[""] * 4 for _ in range(4)]
    #variableName = [["" for c in range(4)] for r in range(4)]
    printGrid(grid)
    while True:
        try:
            text = input('INPUT > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            RUN_GAME(tree, grid, variableName,myset)
