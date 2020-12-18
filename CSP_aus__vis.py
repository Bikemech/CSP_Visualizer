from CSPtest_vis import *
import re
from tkinter import Tk, Canvas
from time import sleep
from random import shuffle

class straya(Canvas):
    def __init__(self):
        self.handle = Tk()
        self.stall = None
        super().__init__(self.handle, height = 500, width = 500)
        self.tiles = {}
        self.tiles["WA"] = self.create_polygon(
            [50, 200, 80, 350, 200, 380, 200, 150], fill = "#FFFFFF", outline="#000000")
        self.tiles["NT"] = self.create_polygon(
            [200, 150, 200, 280, 330, 280, 330, 150], fill = "#FFFFFF", outline="#000000")
        self.tiles["Q"] = self.create_polygon(
            [330, 150, 370, 150, 400, 50, 410, 80, 450, 310, 360, 310, 360, 280, 330, 280], fill="#FFFFFF", outline="#000000")
        self.tiles["NSW"] = self.create_polygon(
            [360, 310, 450, 310, 430, 400, 360, 380], fill="#FFFFFF", outline="#000000")
        self.tiles["V"] = self.create_polygon(
            [430, 400, 360, 380, 360, 450, 410, 450], fill="#FFFFFF", outline="#000000")
        self.tiles["SA"] = self.create_polygon(
            [360, 450, 360, 280, 200, 280, 200, 380], fill="#FFFFFF", outline="#000000")

        self.pack()

    def wait(self):
        self.update()
        if self.stall:
            sleep(self.stall)

    def tile_render(self, tile):
        col = {'R': '#ff0000', 'G': '#0000ff', 'B':'#00ff00'}
        self.itemconfig(self.tiles[tile.label], fill = col[tile.domain[0]])
        self.wait()

    def render(self, tree):
        col = {'R': '#ff0000', 'G': '#0000ff', 'B':'#00ff00'}
        for t in tree:
            if len(t.domain) == 1:
                self.itemconfig(self.tiles[t.label], fill = col[t.domain[0]])
            else:
                self.itemconfig(self.tiles[t.label], fill = "#FFFFFF")
        self.wait()

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
shuffle(tree)

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

t = straya()
t.stall = 0.3


solve(tree, v = t)



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

t.mainloop()