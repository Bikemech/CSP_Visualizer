from CSPtest import *
import re


string = """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """


REG = re.compile(r'(\w+)')
states = {n:node(n) for n in set(REG.findall(string))}

regions = string.split(";")
for reg in regions:
    s = REG.findall(reg.strip())[1:]
    r = REG.match(reg.strip())
    for n in s:
        states[r.group(0)].add_neighbor(states[n])

domain = list('RGB')
states['WA'].domain_propagation(domain.copy())

tree = make_tree(states['WA'])

log = open("aus_prune_csp.txt", 'w')
solve(tree, log=log, prune=True)

snap = []
string = ""

for d in domain:
    print([d])
    string += "%s\n"%d
    for s in tree:
        if s.domain == [d]:
            print(s.label, end = '\t')
            string += "%s  "%s.label
    print()
    string += "\n"

log.write(string)

snap.append(string)

states['WA'].domain_propagation(domain)
solve(tree)



string = ""

for d in domain:
    print([d])
    string += "%s\n"%d
    for s in tree:
        if s.domain == [d]:
            print(s.label, end = '\t')
            string += "%s  "%s.label
    print()
    string += "\n"

snap.append(string)

for i in snap:
    print(i)