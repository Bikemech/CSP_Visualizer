from CSPtest import *
import re

def transpose(matr):
    return [[matr[i][j] for i in range(len(matr[j]))] for j in range(len(matr))]

def assign(tree, m, n):
    for i in tree:
        if i.label == str(m):
            i.domain = [str(n)]
            print("assigned", n)

def result_manifest(tree, matr, cleanup = False):
    for n in tree:
    # print(n)
    # print(n.label, len(n.label))
        for i, row in enumerate(matr):
            for j, p in enumerate(row):
                if p == n.label:
                    if cleanup and len(n.domain) > 1:
                        matr[i][j] = "-"
                    else:
                        matr[i][j] = n.domain[0]

    return matr

def highlight(m, n = None, blackout=False):
    if n:
        print("\tHighlight: ", n)
    r = 0
    print("\t", "-"*23)
    for i in m:
        print("\t", end="|")
        r += 1
        c = 0
        for j in i:
            c += 1
            if j == n:
                print(" #", end = "")
            elif blackout:
                print(" -", end= "")
            else:
                print(" %s"%j, end= "")
            if c % 3 == 0:
                print(" |", end = "")
        print()
        if r % 3 == 0:
            print("\t ", "-"*22)
    print("\n")

string = ""
for i in range(9):
    for j in range(9):
        string += "%d%d:"%(i + 1, j + 1)

        for k in range(9):
            if (i, k) != (i, j):
                string += " %d%d"%(i + 1, k + 1)

            if (k, j) != (i, j):
                string += " %d%d"%(k + 1, j + 1)

        p = (i // 3) * 3
        q = (j // 3) * 3
        for k in range(p, p + 3):
            for l in range(q, q + 3):
                if (i, j) != (k, l):
                    string += " %d%d"%(k + 1, l + 1)

        string += ";\n"


map_string = string

REG = re.compile(r'(\w\w)')
states = {n:node(n) for n in set(REG.findall(string))}

regions = string.split(";")
for reg in regions:
    s = REG.findall(reg.strip())[1:]
    r = REG.match(reg.strip())
    for n in s:
        states[r.group(0)].add_neighbor(states[n])

domain = list('123456789')
states['11'].domain_propagation(domain)

tree = make_tree(states['11'])


a = [21, 51, 61, 32, 82, 13, 23, 34, 44, 84, 15, 25, 55, 85, 95, 26, 66, 76, 87, 97, 28, 78, 49, 59, 89]
b = [1, 6, 5, 3, 4, 2, 6, 7, 8, 1, 6, 2, 5, 9, 3, 4, 2, 8, 5, 2, 9, 1, 9, 8, 3]

# a = [11, 12, 16, 19, 23, 28, 32, 33, 36, 42, 44, 49, 52, 55, 58, 61, 66, 68, 74, 77, 78, 82, 87, 91, 94, 98, 99]
# b = [1, 6, 9, 3, 5, 7, 2, 3, 8, 5, 9, 6, 8, 1, 5, 6, 7, 2, 2, 8, 9, 4, 7, 5, 3, 1, 2]

c = list(zip(a, b))

for i in c:
    assign(tree, i[0], i[1])


log = open('Soduko_csp_opt_log.txt', 'w')
counter = [0]

matr = [["%d%d"%(i, j) for i in range(1, 10)] for j in range(1, 10)]
init_matr = [["%d%d"%(i, j) for i in range(1, 10)] for j in range(1, 10)]
init_matr = result_manifest(tree, init_matr, True)

highlight(matr)

# solve(tree, log=log, queue=smallest_first, prune=True, counter=counter)
solve(tree, log=log, queue=None, prune=False, counter=counter)


for d in domain:
    # print([d])
    string += "%s\n"%d
    for s in tree:
        if s.domain == [d]:
            # print(s.label, end = '\t')
            string += "%s  "%s.label
    print()
    string += "\n"


# for i in matr:
#     print(i)

print("\n\n")



# for n in tree:
#     # print(n)
#     # print(n.label, len(n.label))
#     for i, row in enumerate(matr):
#         for j, p in enumerate(row):
#             if p == n.label:
#                 matr[i][j] = n.domain[0]


matr = result_manifest(tree, matr)

for i in "1234568789":
    highlight(matr, i, True)

highlight(init_matr)

highlight(matr)


print(counter)