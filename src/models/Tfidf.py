#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: largelymfs
# @Date:   2014-12-23 20:06:10
# @Last Modified by:   largelymfs
# @Last Modified time: 2014-12-23 20:07:39

import numpy as np

class TFIDF:

	def __init__(self, filename):
		#get the vocab
		vocab = {}