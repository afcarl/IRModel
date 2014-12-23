#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: largelymfs
# @Date:   2014-12-23 22:03:52
# @Last Modified by:   largelymfs
# @Last Modified time: 2014-12-23 23:23:57
import numpy as np

class ProbModel:
	def __init__(self, filename):
		with open(filename) as fin:
			self.doc = [l.strip().split() for l in fin]
		##get vocab and number of word and doc
		self.number_doc = len(self.doc)
		self.stat = {}
		self.doclen = {}
		self.maxlen = 0
		for (i, doc) in enumerate(self.doc):
			for word in doc:
				if word not in self.stat:
					self.stat[word] = {}
				if i not in self.stat[word]:
					self.stat[word][i] = 1
				else:
					self.stat[word][i] += 1
			self.doclen[i] = len(doc)
			if self.doclen[i] > self.maxlen:
				self.maxlen = self.doclen[i]
	def querry(self, q, t):
		p = {}
		p1 = {}
		for w in q:
			p[w] = 0.5
			if w in self.stat:
				p1[w] = float(len(self.stat[w])+0.5)/(self.number_doc+1.0)
			else:
				p1[w] = 0.0

		for it in range(0, 50):
			sim = [0 for i in range(self.number_doc)]
			for w in q:
				if w in self.stat:
					sets = self.stat[w]
					for id in sets:
						sim[id] += np.log( p[w] / (1-p[w]))
						sim[id] += np.log( (1-p1[w]) / p1[w])
			res = sorted(enumerate(sim), cmp = lambda x, y: -cmp(x[1],y[1]))[:50]
			for w in q:
				tmp = {}
				v= 0
				if w in self.stat:
					sets = self.stat[w]
					for id in sets:
						if res.count(id)>0:
							v+=1
					n = len(sets)
				p[w] = float(v + 0.5) / (50 + 1.0)
				p1[w] = float(n - v + 0.5) / (self.number_doc- 50.0 + 1.0)
		for i in range(t):
			print res[i][0], "".join(self.doc[res[i][0]])

if __name__=="__main__":
	model = ProbModel("./../../data/demo.txt.out")
	model.querry(["进球", "晋级", "胜利"], 10)

