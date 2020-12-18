from CSPtest_vis import *
from random import shuffle, seed
import re
from time import sleep
from tkinter import Tk, Canvas, Scale

class svea_lan(Canvas):
    def __init__(self, poly, order):
        self.handle = Tk()
        self.stall = None
        super().__init__(self.handle, height = 900, width = 600)
        self.tiles = {}
        self.slider = None
        self.solutionstep = []
        self.state = 0
        
        polygons = open(poly, 'r').readlines()
        for i, p in enumerate(polygons):
            polygons[i] = p.strip().split(",")
            for j, r in enumerate(polygons[i]):
                polygons[i][j] = int(r)

        self.tiles = dict(zip(order, polygons))

        for key in self.tiles:
            self.tiles[key] = self.create_polygon(self.tiles[key], fill="#FFFFFF", outline="#000000", width = 6)

        self.pack()

    def wait(self):
        self.update()
        if self.stall:
            sleep(self.stall)

    def tile_render(self, tile):
        col = {'R': '#ff0000', 'B': '#0000ff', 'G':'#00ff00', 'Y':'#ffff00', 'P':'#ff9977'}
        self.itemconfig(self.tiles[tile.label], fill = col[tile.domain[0]])
        self.wait()

    def render(self, tree):
        col = {'R': '#ff0000', 'B': '#0000ff', 'G':'#00ff00', 'Y':'#ffff00', 'P':'#ff9977'}
        for t in tree:
            if len(t.domain) == 1:
                self.itemconfig(self.tiles[t.label], fill = col[t.domain[0]])
            else:
                self.itemconfig(self.tiles[t.label], fill = "#FFFFFF")
        self.wait()

    def save_state(self, tree):
        self.solutionstep.append(deep_copy(tree))

    def complete(self):
        self.slider = Scale(self.handle, from_=0, to=len(self.solutionstep) - 1, orient = 'horizontal', length = 600)
        self.slider.pack()
        self.state = self.slider.get()
        self.stall = None

    def fetch_state(self):
        while self.slider.get() < self.state:
            self.state -= 1
            self.render(self.solutionstep[self.state])

        while self.slider.get() > self.state:
            self.state += 1
            self.render(self.solutionstep[self.state])


def assign(tree, m, n):
    for i in tree:
        if i.label == str(m):
            i.domain = [str(n)]


string = """Lappland: Norrbotten Vasterbotten Jamtland;
            Norrbotten: Lappland Vasterbotten;
            Vasterbotten: Norrbotten Lappland Angermanland;
            Jamtland: Angermanland Medelpad Harjedalen;
            Angermanland: Vasterbotten Jamtland Medelpad Lappland;
            Medelpad: Harjedalen Angermanland Jamtland Halsingland;
            Harjedalen: Halsingland Medelpad Jamtland;
            Halsingland: Medelpad Harjedalen Dalarna Gastrikland;
            Dalarna: Harjedalen Gastrikland Halsingland Varmland Vastmanland;
            Gastrikland: Halsingland Dalarna Vastmanland Uppland;
            Varmland: Dalarna Vastmanland Dalsland Narke Vastergotland;
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
for i in order:
    print(i)

sverige = svea_lan('sverige_polygon.txt', order)
sverige.stall = 0.07


print("\n\n\n")
# seed(30)
# shuffle(tree)

log = open('Sverige_order_prune_queue_log.txt', 'w')
counter = [0]

sverige.render(tree)
sleep(2)

solve(tree, verbose = False, log = log, prune=False, queue=None, counter = counter, v = sverige)
# solve(tree, verbose = False, log = log, prune=True, queue=neighbors_first, counter = counter, v = sverige)

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
sverige.complete()
while True:
    sverige.handle.update()
    sverige.fetch_state()

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
