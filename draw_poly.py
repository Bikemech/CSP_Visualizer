from tkinter import Tk, Canvas
import atexit

class sub_poly:
	def __init__(self, poly):
		self.poly = poly
		self.outline = None
		self.name = None

	def __repr__(self):
		string = ""
		string += str(self.poly)
		string += "\t%s"%self.name
		return string

class canvas(Canvas):
	def __init__(self):
		self.handle = Tk()
		super().__init__(self.handle, height = 800, width = 1000)
		self.pack()
		self.snap = 50;

		self.buffered_click = None
		self.mode = "POLYGON"
		self.temp_lines = []
		self.event_buffer = []
		self.grid = []
		self.polygons = []
		self.poly_data = []

	def draw_grid(self):
		for i in range(0, 1000, self.snap):
			for j in range(0, 800, self.snap):
				self.grid.append(self.create_oval(i - 1, j -1, i - 1, j + 1))

	def adjust_to_grid(self, event):
		return (round(event.x/self.snap) * self.snap, round(event.y/self.snap) * self.snap)

	def click(self, event):
		print(event)

		# if right click:
		if event.num == 3:
			if self.mode == "POLYGON":
				self.buffered_click = None
				self.make_poly()

				return

		if self.mode == "POLYGON":
			self.event_buffer.append(event)
			if self.buffered_click:
				self.temp_lines.append(self.make_line(event, self.buffered_click))
				self.buffered_click = event
				return
			self.buffered_click = event
			return

	def make_poly(self):
		poly = []

		for i in self.temp_lines:
			self.delete(i)

		self.temp_lines = []


		for c in self.event_buffer:
			x, y = self.adjust_to_grid(c)
			poly += [x, y]

		self.polygons.append(self.create_polygon(poly, fill = "#bbbbbb", outline = "#000000", width = 3))
		if len(poly) > 4:
			self.poly_data.append(sub_poly(poly))
		self.event_buffer = []


	def make_line(self, event_a, event_b):
		x1 = round(event_a.x/self.snap) * self.snap
		y1 = round(event_a.y/self.snap) * self.snap

		x2 = round(event_b.x/self.snap) * self.snap
		y2 = round(event_b.y/self.snap) * self.snap

		print(x1, x2, y1, y2)

		return self.create_line((x1, y1, x2, y2), width = 3, fill = "#008833")

def show(g, fname):
	with open(fname, "w") as f:
		for i in g.poly_data:
			f.write(str(i.poly)[1:-1])
			f.write("\n")
	


c = canvas()
c.snap = 10

atexit.register(show, c, "test.txt")

c.draw_grid()
c.handle.bind("<Button>", c.click)

c.mainloop()