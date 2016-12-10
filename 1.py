import random

def whowon():
    global a

    for i in 0, 1, 2:
        row = sum(a[i])
        col = sum([c[i] for c in a])
        if row == 3 or col == 3:
            return 1
        if row == -3 or col == -3:
            return -1
    if a[0][0] == a[1][1] == a[2][2] != 0:
        return a[0][0]
    if a[0][2] == a[1][1] == a[2][0] != 0:
        return a[0][0]
    for i in a:
        if 0 in i:
            return 2
    return 0

def printrow(k):
    global a

    s = " " + str(k) + " │"
    for i in a[k]:
        if i == 1:
            s += " x "
        elif i == -1:
            s += " o "
        else:
            s += "   "
        s += "│"
    print(s)

def printmatrix():
    global a

    s0 = "   ┌───┬───┬───┐"
    s1 = "   ├───┼───┼───┤"
    s2 = "   └───┴───┴───┘"
    print("     A   B   C")
    print(s0)
    printrow(0)
    print(s1)
    printrow(1)
    print(s1)
    printrow(2)
    print(s2)

def bruteforce(c):
    global a

    r = whowon()
    wf = 0
    lf = 0
    tf = 0
    if r != 2:
        return r * c
    for i in 0, 1, 2:
        for j in 0, 1, 2:
            if a[i][j] == 0:
                a[i][j] = c
                r = bruteforce(-c)
                if r == 1:
                    wf = 1
                elif r == 0:
                    tf = 1
                else:
                    lf = 1
                a[i][j] = 0
    if lf:
        return 1
    if tf:
        return 0
    return -1

def mov(c):
    global a

    wf = 0
    lf = 0
    tf = 0
    b = [[-2] * 3, [-2] * 3, [-2] * 3]
    for i in 0, 1, 2:
        for j in 0, 1, 2:
            if a[i][j] == 0:
                a[i][j] = c
                r = bruteforce(-c)
                if r == 1:
                    wf = 1
                    b[i][j] = -1
                elif r == 0:
                    tf = 1
                    b[i][j] = 0
                else:
                    lf = 1
                    b[i][j] = 1
                a[i][j] = 0
    k = -1
    if tf:
        k = 0
    if lf:
        k = 1
    flag = 1
    while flag:
        i, j = random.randint(0, 2), random.randint(0, 2)
        if b[i][j] == k:
            flag = 0
            a[i][j] = c

random.seed()
a = [[0] * 3, [0] * 3, [0] * 3]
print("choose 'x' or 'o'")
c = input()
if c == "o" or c =="0" or c =="O":
    c = -1
else:
    c = 1
if c == -1:
    a[random.randint(0, 2)][random.randint(0, 2)] = 1
while whowon() == 2:
    printmatrix()
    col = row = -1
    while col < 0 or row < 0 or a[row][col] != 0:
        col = row = -1
        print("Your move:")
        s = input()
        for i in 0, 1, 2:
            if str(i) in s:
                row = i
        for i in ("A", 0), ("B", 1), ("C", 2), ("a", 0), ("b", 1), ("c", 2):
            if i[0] in s:
                col = i[1]
    a[row][col] = c
    if whowon() == 2:
        mov(-c)

r = whowon()
printmatrix()
if r == c:
    print("You won... WTF!? IT'S IMPOSSIBLE!")
elif r == 0:
    print("It's tie.")
else:
    print("YOU LOSE! KEK!!!")