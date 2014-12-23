#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: largelymfs
# @Date:   2014-12-23 22:22:05
# @Last Modified by:   largelymfs
# @Last Modified time: 2014-12-23 23:22:43

import numpy as np
class T:
	def __init__(self, logic=0, word=None, children=[]):
		self.logic = logic
		self.word = word
		self.children = children


class ExBM:
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

		mindf = self.number_doc
		self.maxtf = [0 for i in range(self.number_doc)]
		for (k, v) in self.stat.items():
			tmp = len(v)
			if mindf > tmp:
				mindf = tmp
			for (id, cnt) in v.items():
				if self.maxtf[id] < cnt:
					self.maxtf[id]= cnt
		self.maxidf = np.log(float(self.number_doc) / mindf + 1.0)

	def w(self, word, doc):
   		if word in self.stat and doc in self.stat[word]:
   			return float(self.stat[word][doc]) / self.maxtf[doc] * np.log(float(self.number_doc) / len(self.stat[word]) + 1) / self.maxidf
   		else:
   			return 0

	def sim(self, t, doc):
		if t.logic==0:
			return self.w(t.word, doc)
		elif t.logic==3:
			return 1- self.w(t.word, doc)
		elif t.logic==1:
			res = 0
			for ch in t.children:
				tmp = self.sim(ch, doc)
				res += (1.0-tmp)*(1.0-tmp)
			return 1.0-np.sqrt(res/len(t.children))
		else:
			res = 0
			for ch in t.children:
				tmp = self.sim(ch, doc)
				res += tmp * tmp
			return np.sqrt(res /len(t.children))
	def querry(self, t):
		s = [(i, self.sim(t, i)) for i in range(self.number_doc)]
		res = sorted(s, cmp =lambda x, y:-cmp(x[1],y[1]))[:10]
		for (id, score) in res:
			print id, "".join(self.doc[id])

if __name__=="__main__":
	t = T(2, children=[T(word="进球"), T(1, children=[T(word="晋级"), T(word="胜利")])])
	model = ExBM("./../../data/demo.txt.out")
	model.querry(t) 
