from __future__ import division, with_statement
from Tkinter import *
import itertools, random, math

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
			if i % 6 == 0:
				canvas.create_text(width / 2 - bandWidth * i, 375, text=str(self.scale * -i))
		for i in range(len(self.positive)):
			canvas.create_rectangle(width / 2 + bandWidth * i, 350, width / 2 + bandWidth * i + barWidth, 350 - heightRatio * self.positive[i])
			if i % 6 == 0:
				canvas.create_text(width / 2 + bandWidth * i, 375, text=str(self.scale * i))
		root.mainloop()

def readCSV(file):
	with open(file, "r") as fh:
		data = fh.read()
	return [float(x.split(",")[1]) for x in data.split("\n")[1:-1]]
	
def pvalue(value, data, lessThan=True):
	num = 0
	for datum in data:
		if datum < value:
			num += 1
	return num / len(data) if lessThan else 1 - num / len(data)
	
average = lambda x: sum(x) * 1.0 / len(x)
variance = lambda x: map(lambda y: (y - average(x)) ** 2, x)
stdev = lambda x: math.sqrt(average(variance(x)))
		
condition1 = readCSV("related.csv")
condition2 = readCSV("fullControl.csv")

print "condition1 loaded with mean:", average(condition1), ", SD:", stdev(condition1), "and size:", len(condition1)
print "condition2 loaded with mean:", average(condition2), ", SD:", stdev(condition2), "and size:", len(condition2)

#TODO: replace these with two different combinations for each list? or random iterator//have two iterators

def randomize(list, num):
	for i in range(num):
		random.shuffle(list)
		yield list
		
print "Generating all permutations of data.."
permutations = randomize(condition1 + condition2, 100000) #itertools.permutations(condition1 + condition2)
print "Permutation iterator generated"

print "Iterating through permutations and calculating differences in means..."
data = []
i = 0
length = 100000 #factorial(len(condition1) + len(condition2))
for permutation in permutations:
	data += [sum(permutation[:len(condition1)]) / len(condition1) - sum(permutation[len(condition1):]) / len(condition2)]
	if i % (length / 20) == 0: print "\t" + str(i / length * 100) + "%.."
	i += 1
print "Differences calculated"

difference = average(condition1) - average(condition2)
print "Generated p-value set for data:", (pvalue(12.6, data), pvalue(12.6, data, False))

print "Generating histogram.."	
histogram = Histogram(data, scale=1)
print "Histogram with the following distribution generated"

print histogram.positive
print histogram.negative

histogram.graph()