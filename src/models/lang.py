#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: largelymfs
# @Date:   2014-12-23 21:27:44
# @Last Modified by:   largelymfs
# @Last Modified time: 2014-12-23 21:52:18

import numpy as np
class LangModel:
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

	def get_p(self, term, doc):
		tmp = float(self.doclen[doc] + 1) / float(self.maxlen+1)
		if term in self.stat and doc in self.stat[term]:
			return (float(self.stat[term][doc]) + tmp)/(self.doclen[doc]+1.0)
		else:
			return (tmp)/(self.doclen[doc]+1.0)
	def score(self, q, doc):
		tmp = 0.0
		for w in q:
			tmp+= np.log(self.get_p(w, doc))
		return tmp
	def querry(self, q):
		scores = [(i, self.score(q, i)) for i in range(self.number_doc)]
		scores = sorted(scores, cmp=lambda x, y: -cmp(x[1],y[1]))[:10]
		for (id, score) in scores:
			print "".join(self.doc[id])

if __name__=="__main__":
	model = LangModel("./../../data/demo.txt.out")
	model.querry(["足球","晋级"])
