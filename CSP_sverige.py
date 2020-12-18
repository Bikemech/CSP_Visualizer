from CSPtest import *
from random import shuffle, seed
import re

seed(10)

string = """Lappland: Norrbotten Vasterbotten Jamtland;
            Norrbotten: Lappland Vasterbotten;
            Vasterbotten: Norrbotten Lappland Angermanland;
            Jamtland: Angermanland Medelpad Harjedalen;
            Angermanland: Vasterbotten Jamtland Medelpad;
            Medelpad: Harjedalen Angermanland Jamtland Halsingland;
            Harjedalen: Halsingland Medelpad Jamtland;
            Halsingland: Medelpad Harjedalen Dalarna Gastrikland;
            Dalarna: Harjedalen Gastrikland Halsingland Varmland Vastmanland;
            Gastrikland: Halsingland Dalarna Vastmanland Uppland;
            Varmland: Dalarna Vastmanland Dalsland Narke;
            Vastmanland: Varmland Dalarna Gastrikland Uppland Narke Sodermanland;
            Uppland: Gastrikland Vastmanland Sodermanland;
            Dalsland: Varmland Bohuslan Vastergotland;
            Narke: Varmland Vastmanland Sodermanland Vastergotland Ostergotland;
            Sodermanland: Vastmanland Uppland Narke Ostergotland;
            Bohuslan: Dalsland Vastergotland;
            Vastergotland: Dalsland Bohuslan Narke Ostergotland Halland Smaland;
            Ostergotland: Narke Sodermanland Vastergotland Smaland;
            Halland: Vastergotland Smaland Skane;
            Smaland: Vastergotland Ostergotland Halland;
            Skane: Halland Smaland Blekinge;
            Blekinge: Skane Smaland"""


order = []
for i in string.split(";"):
    order.append(i.split(":")[0].strip())

REG = re.compile(r'(\w+)')
states = {n:node(n) for n in set(REG.findall(string))}

regions = string.split(";")
for reg in regions:
    s = REG.findall(reg.strip())[1:]
    r = REG.match(reg.strip())
    for n in s:
        states[r.group(0)].add_neighbor(states[n])

domain = list('RGB')
states['Lappland'].domain_propagation(domain.copy())

tree = make_tree(states['Lappland'])

shuffle(tree)

log = open('Sverige_order_prune_queue_log.txt', 'w')
counter = [0]

# solve(tree, verbose = False, log = log, prune=True, queue=domain_priority, counter = counter)
solve(tree, verbose = False, log = log, prune=True, queue=smallest_neighbor, counter = counter)

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

log.write("\n%s\n"%string)
log.close()

snap.append(string)
print(string)

print(counter)

# states['Lappland'].domain_propagation(domain)
# solve(tree)



# string = ""

# for d in domain:
#     print([d])
#     string += "%s\n"%d
#     for s in tree:
#         if s.domain == [d]:
#             print(s.label, end = '\t')
#             string += "%s  "%s.label
#     print()
#     string += "\n"

# snap.append(string)

# for i in snap:
#     print(i)


# orderletter = [chr(i + 0x61) for i in range(len(order))]

# keys = {order[i]:orderletter[i] for i in range(len(order))}


# conn = set()

# # for i in tree:
# #     for j in i.neighbors:
# #         conn.add("\\draw (%s) -- (%s);"%(keys[i.label], keys[j.label]))

# # for i in conn:
# #     print(i)