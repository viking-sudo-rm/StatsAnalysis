from __future__ import division
from Tkinter import *
from math import factorial
import itertools

class Histogram:

	def __init__(self, data, scale=1):
		self.positive = []
		self.negative = []
		self.scale = scale
		for datum in data:
			l = self.positive if datum >= 0 else self.negative
			i = int(abs(datum // scale))
			if i < len(l):
				l[i] += 1
			else: l.append(1)
			
	def graph(self):
		root = Tk()
		root.title("distribution as histogram")
		canvas = Canvas(root, height=400, width=600)
		canvas.pack()
		
		width = 600
		bandWidth = width / (len(self.positive + self.negative) + 2)
		barWidth = bandWidth / 2
		heightRatio = 300 / max(self.positive + self.negative)
		
		for i in range(1, len(self.negative)):
			canvas.create_rectangle(width / 2 - bandWidth * i, 350, width / 2 - bandWidth * i + barWidth, 350 - heightRatio * self.negative[i])
			canvas.create_text(width / 2 - bandWidth * i, 375, text=str(self.scale * -i))
		for i in range(len(self.positive)):
			canvas.create_rectangle(width / 2 + bandWidth * i, 350, width / 2 + bandWidth * i + barWidth, 350 - heightRatio * self.positive[i])
			canvas.create_text(width / 2 + bandWidth * i, 375, text=str(self.scale * i))
		root.mainloop()

condition1 = [80, 40, 70, 50, 60, 80, 40, 70, 50, 60,80, 40, 70, 50, 60,80, 40, 70, 50, 60,80, 40, 70, 50, 60]
condition2 = [10, 54, 72, 54, 41]

#TODO: replace these with two different combinations for each list?

print "Generating all permutations of data.."
permutations = itertools.permutations(condition1 + condition2)
print "Permutation iterator generated"

print "Iterating through permutations and calculating differences in means..."
data = []
i = 0
length = factorial(len(condition1) + len(condition2))
for permutation in permutations:
	data += [sum(permutation[:len(condition1)]) / len(condition1) - sum(permutation[len(condition1):]) / len(condition2)]
	if i % (length / 20) == 0: print "\t" + str(i / length * 100) + "%.."
	i += 1
print "Differences calculated"

print "Generating histogram.."	
histogram = Histogram(data, scale=4)
print "Histogram with the following distribution generated"

print histogram.positive
print histogram.negative

histogram.graph()