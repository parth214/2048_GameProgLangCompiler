import random
import sys
import copy

def newEmpty(size):
    return [[0 for i in range(0, size)] for i in range(0, size)]
    
def traverse(a, f):
    for line in a:
        for ele in line:
            if f(ele): return True
    return False

def randomPoint(size):
    x = random.randint(0, size)
    y = random.randint(0, size)
    return (x, y)

def all_filled(grid):
    flag=True
    for i in range(4):
        for j in range(4):
            if(grid[i][j]==0):
                flag=False
                return flag
    return flag


def randomInit(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    v = random.randint(0, len(seed)-1)
    a[x][y] = seed[v]

def randomNum(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    if a[x][y] == 0:
        v = random.randint(0, len(seed)-1)
        a[x][y] = seed[v]
    else: randomNum(a)

def random_tile_generator(grid):
    if(all_filled(grid)==True):
        return 
    while True:
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        if grid[row][column] == 0:
            grid[row][column] = random.choice([2,4])
            break

def printGrid(grid):
    for i in range(4):
        for j in range(4):
            print(grid[i][j], end='\t')
        print()

def reverse(mat):
    new_mat=[]
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3-j])
    return new_mat

def transp(mat):
    new_mat=[[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            new_mat[i][j]=mat[j][i]
    return new_mat

def shift(grid, variableName):
    row=0
    while row<=3:
        col=0
        while col<=3:
            k=row
            while(k<4 and grid[k][col]==0):
                k+=1
            if (k != row and k<4):
                grid[row][col], grid[k][col] = grid[k][col], 0
                variableName[row][col], variableName[k][col] = variableName[k][col], ""
            col+=1
        row+=1

def isWin(a):
    return traverse(a, lambda x: x == 2048)

def isFail(a):
    def aux(a):
        for i in a:
            for j in zip(i, i[1:]):
                if j[0] == 0 or j[1] == 0 or j[0] == j[1]: return False
        return True
    return aux(a) and aux(rotate(a))
    
def check_to_add_or_not(variableName,i,j):
    if (variableName[i][j]=="" and variableName[i+1][j] != ""):
        variableName[i][j]+=variableName[i+1][j]
    elif (variableName[i][j]!="" and variableName[i+1][j] != ""):
        variableName[i][j]+= "," + variableName[i+1][j]

def add_it(grid,i,j):
    grid[i][j]=2*grid[i][j]

def sub_it(grid,i,j):
    grid[i][j]=0

def mul_it(grid,i,j):
    grid[i][j]=grid[i][j]*grid[i][j]

def div_it(grid,i,j):
    grid[i][j]=1  

def make_zero_after_merging(grid,variableName,i,j):
    grid[i+1][j]=0
    variableName[i+1][j]=""

def rotate(n, grid,variableName):
    for i in range(0,n):
        temp1=copy.deepcopy(grid)
        temp2=copy.deepcopy(variableName)
        for i in range(0,4):
            for j in range(0,4):
                grid[i][3-j] = temp1[j][i]
                variableName[i][3-j] = temp2[j][i]

def merge(grid, operation, variableName,myset):
    for i in range(0,3):
        for j in range(0,4):
            if(grid[i][j] != 0 and grid[i][j] == grid[i+1][j]):
                if operation == 'ADD':
                    add_it(grid,i,j)
                    check_to_add_or_not(variableName,i,j)
                elif operation =='SUBTRACT':
                    sub_it(grid,i,j)
                    my_var_names=variableName[i][j]
                    splitted=my_var_names.split(",")
                    for var_name in splitted:
                        if var_name in myset:
                            myset.remove(var_name)

                    my_var_names2=variableName[i+1][j]
                    splitted2=my_var_names2.split(",")
                    for var_name2 in splitted2:
                        if var_name2 in myset: 
                            myset.remove(var_name2)
                    variableName[i][j]=""
                elif operation=='MULTIPLY':
                    mul_it(grid,i,j)
                    check_to_add_or_not(variableName,i,j)
                elif operation=='DIVIDE':
                    div_it(grid,i,j)
                    check_to_add_or_not(variableName,i,j)
                make_zero_after_merging(grid,variableName,i,j)



def processOperation(operation,move,grid,variableName,myset):
    if(move=="UP"):
        rotate(0, grid,variableName)
        shift(grid, variableName)
        merge(grid,operation,variableName,myset)
        shift(grid,variableName)
        rotate(4, grid,variableName)
    elif move=="LEFT":
        rotate(1, grid,variableName)
        shift(grid, variableName)
        merge(grid,operation,variableName,myset)
        shift(grid,variableName)
        rotate(3, grid,variableName)
    elif move=="DOWN":
        rotate(2, grid,variableName)
        shift(grid, variableName)
        merge(grid,operation,variableName,myset)
        shift(grid,variableName)
        rotate(2, grid,variableName)
    elif move=="RIGHT":
        rotate(3, grid,variableName)
        shift(grid, variableName)
        merge(grid,operation,variableName,myset)
        shift(grid,variableName)
        rotate(1, grid,variableName)

def printGridStderr(grid, variableName):
    for row in grid:
        for num in row:
            sys.stderr.write(str(num)+" ")
    for i in range(4):
        for j in range(4):
            if variableName[i][j] != "":
                sys.stderr.write(str(i+1)+","+str(j+1)+str(variableName[i][j])+" ")
    sys.stderr.write("\n")

