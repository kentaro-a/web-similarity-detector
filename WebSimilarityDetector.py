# -*- coding: utf-8 -*-

from pprint import pprint
import os, sys, re, csv, requests, datetime, traceback
import numpy as np
from pyquery import PyQuery as pq
import difflib


class WebSimilarityDetector(object):


	"""
		Initialize.
	"""
	def __init__(self):
		pass


	"""
		Make divisions of text for copy-check.
	"""
	def makeDivisions(self, text, min_word_count=20):
		ret = []
		split1 = [t.strip() for t in text.split("。") if re.search("^[\s　]+$", t) is None]
		for s1 in split1:
			split2 = [t.strip() for t in s1.split("、") if re.search("^[\s　]+$", t) is None]
			tmp = []
			for i,s2 in enumerate(split2):
				tmp.append(s2)
				tmp2 = "、".join(tmp)
				if len(tmp2) > min_word_count:
					ret.append(tmp2)
					tmp = []

				# Append if loop count equals last index of loop.
				if (i == len(split2)-1) and (len(tmp) > 0 and len(tmp2) > 0):
					ret.append(tmp2)

		return ret



	"""
		Execute crawling.
	"""
	def crawlGoogle(self, query, page=1, min_similarity=0.7):
		ret = []
		BASE_URL_GOOGLE = "https://www.google.co.jp/search"

		# Get page index(page=1 then pageindex=0, page=2 then pageindex=10, ...)
		def pageIndex(page):
			return ((page-1) * 10)

		# Request parameters.
		params = {
			"q": query,
			"start": pageIndex(page),
		}

		try:
			# Send http-request and get result.
			res = requests.get(BASE_URL_GOOGLE, params=params)

			if res.status_code != 200:
				print("Error: " + "Status({0}) code is invalid.".format(r.status_code))
				self.errorlog(self, "Error: " + "Status({0}) code is invalid.".format(r.status_code))
				return False

			html = res.text

			if html != "":
				doc = pq(html)

				# Block of each Sites on Serps.
				for tag in doc("div#search > div#ires div.g"):
					url = pq(tag).find("h3.r > a")
					url = pq(url).attr("href").replace("/url?q=", "") if pq(url).attr("href") is not None else "Unknown."
					url = re.sub("&sa=.*$","",url)

					desc_tag = pq(tag).find("div.s span.st")
					desc = pq(desc_tag).html()
					desc_bolds = pq(desc_tag).find("b")

					# Fetch the bold phrases.
					bolds = [pq(b).text() for b in desc_bolds]
					bolds = "".join(bolds)

					ratio = difflib.SequenceMatcher(None, self.extrim(params["q"]), self.extrim(bolds)).ratio()

					# Check if query is similar to descriptions.
					# if self.extrim(params["q"]) in self.extrim(desc) or ratio > min_similarity:
					if ratio >= min_similarity:
						ret.append({"query":params["q"], "url":url, "desc":desc, "ratio":ratio})

				self.operationlog(query)
				return ret

			else:
				# If response is empty.
				print("Error: " + "Response html is Empty.")
				self.errorlog("Response html is Empty.")
				return False

		except Exception as e:
			print("Exception: \n" + traceback.format_exc())
			self.errorlog(traceback.format_exc())
			return False


	def extrim(self, text):
		return re.sub("[\s]+", "", text)


	def errorlog(self, log):
		pfx = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
		log_file = os.path.join(os.path.dirname(__file__) + "/logs", 'error_{0}.log'.format(pfx.split(" ")[0]))
		with open(log_file, "a") as f:
			f.write("\n\n{0}\n".format(pfx) + log)


	def operationlog(self, log):
		pfx = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
		log_file = os.path.join(os.path.dirname(__file__) + "/logs", 'operation_{0}.log'.format(pfx.split(" ")[0]))
		with open(log_file, "a") as f:
			f.write("\n\n{0}\n".format(pfx) + log)
