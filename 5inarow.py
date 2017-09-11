def bf_one_row(s):
    if len(s) < 5:
        return 0, 0, 0
    if s.find("xxxxx") != -1:
        return 1000000, 0, 0
    if s.find(".xxxx.") != -1:
        return 30000, 0, 1
    if s.find("xxx.x.xxx") != -1 or s.find("x.xxx.x") != -1 or s.find("xx.xx.xx") != -1:
        return 3000, 0, 1
    is3 = is4 = 0
    for i in range(len(s)):
        p = s[:i] + "x" + s[i + 1:]
        if p.find("xxxxx") != -1:
            is4 += 1
        elif p.find(".xxxx.") != -1:
            is3 += 1
    if is3 > 0 or is4 > 0:
        return 1000 + 10 * (is3 + is4), is3, is4
    count = 0
    for i in range(len(s)):
        for j in range(len(s)):
            mmin = min(i, j)
            mmax = max(i, j)
            p = s[:mmin] + "x" + s[mmin + 1 : mmax] + ("x" if i != j else "") + s[mmax + 1:]
            if p.find("xxxxx") != -1 or p.find(".xxxx.") != -1:
                count += 1
                break
    return 10 * count, 0, 0

def create_patterns():
    global patterns
    for i in range(2 ** 16):
        x = bin(i)[3:]
        x = x.replace("0", ".")
        x = x.replace("1", "x")
        patterns.append(bf_one_row(x))

def parse_one_row(s):
    i = c = 0
    points = [0, 0]
    is3 = [0, 0]
    is4 = [0, 0]
    ox = [1, 1]
    for x in s:
        if c != x != 0:
            if c == 1:
                p = patterns[ox[1]]
                points[1] += p[0]
                is3[1] += p[1]
                is4[1] += p[2]
            if c == -1:
                p = patterns[ox[0]]
                points[0] += p[0]
                is3[0] += p[1]
                is4[0] += p[2]
            c = x
            if c == 1:
                ox = [1, 2 ** i]
            if c == -1:
                ox = [2 ** i, 1]
        if c == 1:
            ox[1] *= 2
        if c == -1:
            ox[0] *= 2
        if 0 != x == c:
            if c == 1:
                ox[1] += 1
            else:
                ox[0] += 1
        if x == 0:
            i += 1
        else:
            i = 0
    if c == 1:
        p = patterns[ox[1]]
        points[1] += p[0]
        is3[1] += p[1]
        is4[1] += p[2]
    if c == -1:
        p = patterns[ox[0]]
        points[0] += p[0]
        is3[0] += p[1]
        is4[0] += p[2]
    return points[1] - points[0], is3 + is4

def print_matrix(matrix):
    s = "    "
    for i in range(15):
        s += " " + chr(ord("A") + i)
    print(s)
    for i in range(15):
        s = str(i).rjust(3) + " "
        for j in matrix[i]:
            s += " "
            if j == -1:
                s += "O"
            elif j == 0:
                s += "·"
            else:
                s += "X"
        print(s)

class Board:
    n = 0
    c = -1
    sum_points = 0
    off = 0
    set3 = [[set(), set()] for i in range(4)]
    set4 = [[set(), set()] for i in range(4)]
    possible_moves = set()

    matrix = [[0] * 15 for i in range(15)]
    cols = [[0] * 15 for i in range(15)]
    diagx = [[0] * min(i + 1, 29 - i) for i in range(29)]
    diagy = [[0] * min(i + 1, 29 - i) for i in range(29)]

    matrix_p = [0] * 15
    cols_p = [0] * 15
    diagx_p = [0] * 29
    diagy_p = [0] * 29

    story = []

    def make_move(self, x, y):
        self.n += 1
        self.c = -self.c

        dx = 14 + x - y
        dy = x + y
        coord = [x, y, dx, dy]
        elem_story = [self.sum_points, self.off]
        r3 = [[0, 0] for i in range(4)]
        r4 = [[0, 0] for i in range(4)]
        self.sum_points -= (self.matrix_p[x] + self.cols_p[y] + self.diagx_p[dx] + self.diagy_p[dy] + self.off)
        for i in range(4):
            for j in 0, 1:
                r3[i][j] = coord[i] in self.set3[i][j]
                r4[i][j] = coord[i] in self.set4[i][j]
                self.set3[i][j].discard(coord[i])
                self.set4[i][j].discard(coord[i])
        elem_story += [r3, r4, [x, self.matrix_p[x]], [y, self.cols_p[y]], [dx, self.diagx_p[dx]], [dy, self.diagy_p[dy]]]

        self.matrix[x][y] = self.c
        self.cols[y][x] = self.c
        self.diagx[dx][min(x, y)] = self.c
        self.diagy[dy][min(14 - x, y)] = self.c

        arr34 = [0] * 4
        self.matrix_p[x], arr34[0] = parse_one_row(self.matrix[x])
        self.cols_p[y], arr34[1] = parse_one_row(self.cols[y])
        self.diagx_p[dx], arr34[2] = parse_one_row(self.diagx[dx])
        self.diagy_p[dy], arr34[3] = parse_one_row(self.diagy[dy])

        self.sum_points += (self.matrix_p[x] + self.cols_p[y] + self.diagx_p[dx] + self.diagy_p[dy])
        for i in range(4):
            if arr34[i][0] > 0:
                self.set3[i][0].add(coord[i])
            if arr34[i][1] > 0:
                self.set3[i][1].add(coord[i])
            if arr34[i][2] > 0:
                self.set4[i][0].add(coord[i])
            if arr34[i][3] > 0:
                self.set4[i][1].add(coord[i])
        m = [0, 0]
        for i in 0, 1:
            if sum([len(a[i]) for a in self.set3]) > 0:
                m[i] = 3
            if sum([len(a[i]) for a in self.set4]) > 0:
                m[i] = 4
        if self.c == -1:
            m = m[::-1]
        self.off = -self.c * 300000 if 0 < m[0] >= m[1] else 0
        self.sum_points += self.off

        self.possible_moves.discard((x, y))
        qset = set()
        xmin, xmax = max(0, x - 2), min(15, x + 3)
        ymin, ymax = max(0, y - 2), min(15, y + 3)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                if (i, j) not in self.possible_moves and self.matrix[i][j] == 0:
                    qset.add((i, j))
        self.possible_moves |= qset

        elem_story.append(qset)
        self.story.append(elem_story)

    def remove(self):
        self.n -= 1
        self.c = -self.c

        elem_story = self.story.pop()
        self.sum_points, self.off = elem_story[:2]
        x, y, dx, dy = coord = [elem_story[i][0] for i in range(4, 8)]
        r3, r4 = elem_story[2:4]
        for i in range(4):
            for j in 0, 1:
                if r3[i][j]:
                    self.set3[i][j].add(coord[i])
                else:
                    self.set3[i][j].discard(coord[i])
                if r4[i][j]:
                    self.set4[i][j].add(coord[i])
                else:
                    self.set4[i][j].discard(coord[i])

        self.matrix_p[x], self.cols_p[y], self.diagx_p[dx], self.diagy_p[dy] = [elem_story[i][1] for i in range(4, 8)]

        self.matrix[x][y] = 0
        self.cols[y][x] = 0
        self.diagx[dx][min(x, y)] = 0
        self.diagy[dy][min(14 - x, y)] = 0

        self.possible_moves -= elem_story[8]
        self.possible_moves.add((x, y))

def choose_move(n, k, alpha):
    global brd
    if n == 0:
        return brd.sum_points
    c = -brd.c
    p = -10000000
    x = y = 0
    if n == 1:
        arr = brd.possible_moves
    else:
        arrr = []
        for (i, j) in brd.possible_moves:
            brd.make_move(i, j)
            arrr.append((choose_move(n - 2, 0, 500000) * c, i, j))
            brd.remove()
        arrr.sort()
        arr = [(a[1], a[2]) for a in reversed(arrr)]
    for (i, j) in arr:
        brd.make_move(i, j)
        pp = brd.sum_points * c
        if pp > 500000:
            if k == 0:
                brd.remove()
            else:
                print(i, chr(ord("A") + j), sep = "")
            return 600000 * c
        if pp > -500000:
            points = choose_move(n - 1, 0, min(-p, 500000)) * c if n > 1 else pp
        else:
            points = -600000
        if points > p:
            p = points
            x, y = i, j
        brd.remove()
        if p >= alpha:
            break
    if k == 1:
        brd.make_move(x, y)
        print(x, chr(ord("A") + y), sep = "")
    return p * c

patterns = []
print("creating of patterns...")
create_patterns()

brd = Board()

print("choose 'x' or 'o'")
c = input()
if c == "o" or c =="0" or c =="O":
    c = -1
    brd.make_move(7, 7)
else:
    c = 1
while abs(brd.sum_points) < 500000:
    print_matrix(brd.matrix)
    y = x = -1
    while y < 0 or x < 0 or brd.matrix[x][y] != 0:
        y = x = -1
        print("Your move:")
        s = input()
        if "r" in s and brd.n >= 2:
            brd.remove()
            brd.remove()
            print_matrix(brd.matrix)
            continue
        for i in range(15):
            if str(i) in s:
                x = i
            if chr(ord("A") + i) in s or chr(ord("a") + i) in s:
                y = i
    brd.make_move(x, y)
    if abs(brd.sum_points) < 500000:
        choose_move(3, 1, 500000)

print_matrix(brd.matrix)
if c * brd.sum_points > 0:
    print("YOU WIN!")
else:
    print("YOU LOSE!")