#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: largelymfs
# @Date:   2014-12-23 20:06:10
# @Last Modified by:   largelymfs
# @Last Modified time: 2014-12-23 23:18:08

import numpy as np
import numpy.linalg as LA
class TFIDF:

	def __init__(self, filename):
		#get the self.vocab
		self.vocab = {}
		id = 0
		doc = 0
		with open(filename) as fin:
			self.doc = [l.strip().split() for l in fin]
		for words in self.doc:
			for word in words:
				if word not in self.vocab:
					self.vocab[word] = id
					id+=1
			doc+=1
		self.word_number = id
		self.doc_number = doc
		self.matrix = np.zeros((self.doc_number, self.word_number))
		self.idf = {}
		for words in self.doc:
			now = set(words)
			for word in now:
				word_id = self.vocab[word]
				if word_id not in self.idf:
					self.idf[word_id] = 1
				else:
					self.idf[word_id] +=1
		for k in self.idf.keys():
			self.idf[k] = np.log((float(self.doc_number) /  float(self.idf[k])))
		id = 0
		for words in self.doc:
			total = 0.0
			for word in words:
				self.matrix[id][self.vocab[word]] +=1.0
				total +=1.0
			if total==0:
				print words
				continue
			self.matrix[id] = self.matrix[id] * (1./total)
			id+=1
		self.matrix = self.matrix.T
		for i in range(self.word_number):
			self.matrix[i] = self.matrix[i]  * (self.idf[i])
		self.matrix = self.matrix.T
	def get_score(self, v1, v2):
		return np.dot(v1, v2)/(LA.norm(v1) * LA.norm(v2))
	def querry(self, q):
		vector = np.zeros(self.word_number)
		total = 0.0
		for w in q:
			if w in self.vocab:
				vector[self.vocab[w]]+=1.0
				total +=1.0
		vector = vector * (1./total)
		for i in range(self.word_number):
			vector[i] *= (self.idf[i])
		result = [(i, self.get_score(self.matrix[i], vector)) for i in range(self.doc_number)]
		result = sorted(result, cmp=lambda x, y:-cmp(x[1],y[1]))[:10]
		for (id, score) in result:
			print id, "".join(self.doc[id])


if __name__=='__main__':
	model = TFIDF("./../../data/demo.txt.out")
	model.querry(["进球", "晋级", "胜利"])