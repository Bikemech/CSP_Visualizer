from random import shuffle, seed

class node:
	def __init__(self, label):
		self.label = label
		self.domain = None
		self.neighbors = []
		self.inference = None

	def __repr__(self):
		string = "%s\t"%self.label
		string += self.domain.__repr__()
		string += '\t'
		return string

	def __lt__(self, other):
		if not self.domain:
			if not other.domain:
				return False
			return True
		return len(self.domain) < len(other.domain)

	def add_neighbor(self, other):
		if other not in self.neighbors:
			self.neighbors.append(other)
			other.neighbors.append(self)

	def domain_propagation(self, dom):
		if self.domain != dom:
			self.domain = dom[:]
			for i in self.neighbors:
				i.domain_propagation(dom)

	def prune_neighbors(self):
		if len(self.domain) > 1:
			return

		d = self.domain[0]

		for n in self.neighbors:
			if d in n.domain:
				n.domain.remove(d)

		# print(self, self.neighbors)


def make_tree(root, nodes = []):
	nodes.append(root)
	ptr = root
	for i in ptr.neighbors:
		if i not in nodes:
			make_tree(i, nodes)
	return nodes	


def check_conflict(a, b):
	if a == b.domain:
		return True
	return False

def check_neighbors(a, node):
	for i in node.neighbors:
		if check_conflict(a, i):
			return True
	return False



def solve(tree, dep = 0, prune=False, verbose = False, log = None, queue=None, counter = None):
	if counter:
		counter[0] += 1
	if queue is not None:
		tree = queue(tree)

	if log:
		log.write("Current state:\ndepth: %d\tElements to assign: %d\n%s\n"%(dep, len(tree), tree))

	if verbose:
		print("Current state:\ndepth:%d\n%s\n"%(dep, tree))

	snapshot = {n:n.domain[:] for n in tree}
	root = tree[0]
	for d in root.domain:
		if not check_neighbors([d], root):
			root.domain = [d]
			if prune:
				root.prune_neighbors()
				print(tree)
			result = {root:d}
			if len(tree) <= 1:
				return result

			if log:
				log.write("Assigned %s\n\n"%tree[0].__repr__())

			if verbose:
				print("Assigned %s\n\n"%tree[0].__repr__())
			lookahead = solve(tree[1:], dep + 1, prune=prune, verbose=verbose, log=log, queue=queue, counter=counter)
			if lookahead is not None:
				result.update(lookahead)
				return result
		# restore domain values
		for n in snapshot:
			n.domain = snapshot[n]
		if log:
			log.write('\n\t### BACKTRACKING TO DEPTH: %d ###\n\n'%dep)
		if verbose:
			print('\t### BACKTRACKING TO DEPTH: %d ###'%(dep - 1))


	return None



def domain_priority(tree):
	return sorted(tree)

def smallest_first(tree):
	val = len(tree[0].domain)
	index = 0
	for i, n in enumerate(tree):
		if n.domain:
			if len(n.domain) < val:
				index = i
				val = len(n.domain)

	if index:
		ptr = tree.pop(index)
		tree.insert(0, ptr)

	return tree

# from random import randint

# a = [node(chr(i + 0x61)) for i in range(5)]
# for n in a:
# 	n.domain = list(set([chr(randint(0x61, 0x64)) for i in range(4)]))
# print(a)
# print(smallest_first(a))