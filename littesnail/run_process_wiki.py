# -*- coding: utf-8 -*-
import sys
import os
from snownlp import SnowNLP

def wiki_extract(zipped_path, out_dir_path):
	print "This may take hours...."
	os.system('bzcat %s| python WikiExtractor.py -b2000M -o %s '%(zipped_path, out_dir_path))
	print 'Done!'
	return

contains_lines = [
	"<noinclude>","boilerplate seealso noprint\">","-{}-","-{”}-","</dl>","boilerplate further noprint\">"
]
whole_line_clean = {
	"[]", "外部链接."
}
starts_clean = [
	"-{"
]

def post_cleaning(line):
	global contains_lines
	global whole_line_clean
	global starts_clean
	for cl in starts_clean:
		if line.startswith(cl):
			return ""
	for cl in whole_line_clean:
		if line == cl:
			return ""
	for cl in contains_lines:
		line = line.replace(cl, "")
	return line

def merge_brackers(input_path, output_path):
	prev_line = ""
	fout = open(output_path, "w")
	for line in open(input_path):
		line = line.strip().decode('UTF-8')
		if line.endswith(u"--"):
			prev_line += line[0:-len(u"--")]
		else:
			prev_line += line
			fout.write(prev_line.encode("UTF-8") + "\n")
			prev_line = ""
	fout.flush()
	fout.close()
	return

def jianfan_convert(input_path, output_path):
	items = {}
	fout = open(output_path, "w")
	for line in open(input_path):
		line = post_cleaning(line).strip()
		if len(line) == 0:
			continue
		s = SnowNLP(line.strip().decode("UTF-8"))
		fout.write(s.han.encode('UTF-8') + "\n")
	fout.flush()
	fout.close()
	return


if True:
	text_path = "../data/wiki-only-text.txt"
	merge_path = "../data/wiki-merge.txt"
	simpified_path = "../data/wiki-simpified.txt"
	merge_brackers(text_path, merge_path)
	jianfan_convert(merge_path, simpified_path)