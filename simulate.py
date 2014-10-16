from __future__ import division
from Tkinter import *
from math import factorial
import itertools, random

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

condition1 = [80, 80, 40, 4, 2, 4, 5, 1, 24, 123, 123, 35, 5, 1, 34, 1, 543, 1, 35, 2, 53, 35, 35, 356, 563]
condition2 = [10, 54, 72, 54, 41, 356, 345, 234, 64, 75, 34, 23, 324, 45, 24, 456, 24, 243, 346, 32, 234, 46, 234, 426, 234, 2346, 324]

#TODO: replace these with two different combinations for each list? or random iterator//have two iterators

def randomize(list, num):
	for i in range(num):
		random.shuffle(list)
		yield list

print "Generating all permutations of data.."
permutations = randomize(condition1 + condition2, 1000000) #itertools.permutations(condition1 + condition2)
print "Permutation iterator generated"

print "Iterating through permutations and calculating differences in means..."
data = []
i = 0
length = 1000000 #factorial(len(condition1) + len(condition2))
for permutation in permutations:
	data += [sum(permutation[:len(condition1)]) / len(condition1) - sum(permutation[len(condition1):]) / len(condition2)]
	if i % (length / 20) == 0: print "\t" + str(i / length * 100) + "%.."
	i += 1
print "Differences calculated"

print "Generating histogram.."	
histogram = Histogram(data, scale=10)
print "Histogram with the following distribution generated"

print histogram.positive
print histogram.negative

histogram.graph()