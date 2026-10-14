import pathlib
import math
inversabil:bool = 1

def get_number(s:str) -> float:
    sign:float = 1
    number:float = 1.0
    start = 0
    
    if s[0] == '-':
        sign = -1
        start = 1
    elif s[0] == '+':
        start = 1

    if (not('0' <= s[start] and s[start] <= '9')):
        return number*sign

    number = 0.0
    for i in range(start, len(s)):
        if (not('0' <= s[i] and s[i] <= '9')): break #nu e cifra
        number = number*10 + float(s[i])
    return number*sign
    
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    file = open(path, "r")
    A: list[list[float]] = []
    B: list[float] = []
    for line in file:
        words = line.split()
        if len(words) == 0: continue
        wordX = words[0]
        wordY = words[1] + words[2]
        wordZ = words[3] + words[4]
        result = words[6]

        a = get_number(wordX)
        b = get_number(wordY)
        c = get_number(wordZ)

        A.append([a,b,c])
        B.append(float(result))
    file.close()
    return A, B

def determinant(matrix: list[list[float]]) -> float:
    global inversabil
    ans: float = 0
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    for j in range(n):
        plus = matrix[0][j] #termenul de pe prima linie
        lin = 1
        col = (j+1)%n
        for i in range(n-1):
            plus *= matrix[lin][col]
            lin = (lin+1)%n
            col = (col+1)%n
        minus = matrix[0][j]
        lin = 1
        col = (j-1+n)%n
        for i in range(n-1):
            minus *= matrix[lin][col]
            lin = (lin+1)%n
            col = (col-1+n)%n
        ans += (plus - minus)
    if ans == 0: 
        inversabil = 0
    return ans

def trace(matrix: list[list[float]]) -> float: #trace
    n = len(matrix)
    ans:float = 0
    for i in range(n):
        ans += matrix[i][i]
    return ans

def norm(vector: list[float]) -> float: #norma
    ans:float = 0
    n = len(vector)
    for i in range(n):
        ans += vector[i]*vector[i]
    return math.sqrt(ans)

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    ans = []
    for i in range(n):
        rand = []
        for j in range(n):
            rand.append(matrix[j][i])
        ans.append(rand)
    return ans

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(matrix)
    ans = []
    for i in range(n): # setez linia
        termen = 0
        for j in range(n):
            termen += matrix[i][j] * vector[j]
        ans.append(termen)
    return ans

def replaced_column_matrix(matrix: list[list[float]], vector: list[float], index:int) -> list[list[float]]:
    n = len(matrix)
    ans = []
    for i in range(n):
        rand = []
        for j in range(n):
            if (j == index): #inlocuiesc coloana index
                rand.append(vector[i])
            else: rand.append(matrix[i][j])
        ans.append(rand)
    return ans

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    numitor = determinant(matrix)
    if (numitor == 0):
        return
    n = len(matrix)
    ans = []
    for j in range(n):
        Ax = replaced_column_matrix(matrix, vector, j)
        numarator = determinant(Ax)
        ans.append(numarator/numitor)
    return ans

def minor(matrix: list[list[float]], i:int, j:int) -> list[list[float]]:
    ans = []
    n = len(matrix)
    for lin in range(n):
        if (lin == i): continue
        rand = []
        for col in range(n):
            if (col == j): continue
            rand.append(matrix[lin][col])
        ans.append(rand)
    return ans

def cofactor(matrix:list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    ans = []
    for i in range(n):
        rand = []
        for j in range(n):
            Mij = minor(matrix, i, j)
            if ((i+j)%2 == 0):
                rand.append(determinant(Mij))
            else:
                rand.append(-determinant(Mij))
        ans.append(rand)
    return ans

def adjoint(matrix: list[list[float]]) -> list[list[float]]: #transpusa lui cofactor
    return transpose(cofactor(matrix))

def inverse(matrix: list[list[float]]) -> list[list[float]]:
    det:float = determinant(matrix)
    ans = adjoint(matrix)
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            ans[i][j] = ans[i][j] / det
    return ans

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    inv = inverse(matrix)
    return multiply(inv, vector)

if (__name__ == "__main__"):
    A, B = load_system(pathlib.Path("input1.in")) #matrice, vector rezultat
    print(f"{A=} {B=}")
    print(f"{determinant(A)=}")
    print(f"{trace(A)=}")
    print(f"{norm(B)=}")
    if (inversabil == 1):
        print(f"{transpose(A)=}")
        print(f"{multiply(A, B)=}")
        print(f"{solve_cramer(A, B)=}")
        print(f"{solve(A, B)=}")
    else: 
        print("Matricea nu este inversabilă (determinantul este 0)")