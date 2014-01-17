#!/usr/bin/env python
""" This script generates minified version of css 
and js files using yui compressor.
Declare folder paths in the script and 
it will generate a min folder with respective minified and log files."""

import sys
import os
import glob
import shutil
import os.path
import argparse
import time

#Store the time the script starts
START_TIME = time.time()
TOTAL_FILES_COMPRESSED = 0
TOTAL_JS_FILES_COMPRESSED = 0
TOTAL_CSS_FILES_COMPRESSED = 0

JSMINPATH = 'min/js'
JSDEVPATH = 'js'
CSSDEVPATH = 'css'
CSSMINPATH = 'min/css'
YUICOMPRESSORPATH = 'yuicompressor.jar'

ENABLE_LOG = False
RETVAL = os.getcwd()

TOTAL_WARNINGS = 0
TOTAL_ERRORS = 0



def log_error_warning(filepath):
	global TOTAL_WARNINGS
	global TOTAL_ERRORS
	logf = open(filepath)
	warning_count = 0
	error_count = 0
	for line in logf:
		if "[ERROR]" in line:
			error_count = error_count + 1
			TOTAL_ERRORS = TOTAL_ERRORS + 1
		if "[WARNING]" in line:
			warning_count = warning_count + 1
			TOTAL_WARNINGS = TOTAL_WARNINGS + 1
	logf.close()
	log_output("Errors " + str(error_count) + " Total Warnings " + str(warning_count))

def log_output(text):
	print text

def increment_compressed_filecount():
	global TOTAL_FILES_COMPRESSED
	TOTAL_FILES_COMPRESSED = TOTAL_FILES_COMPRESSED + 1

def increment_compressed_jfilecount():
	global TOTAL_JS_FILES_COMPRESSED
	TOTAL_JS_FILES_COMPRESSED = TOTAL_JS_FILES_COMPRESSED + 1

def increment_compressed_cfilecount():
	global TOTAL_CSS_FILES_COMPRESSED
	TOTAL_CSS_FILES_COMPRESSED = TOTAL_CSS_FILES_COMPRESSED + 1

def minify_js():
	
	if not os.path.exists(JSMINPATH + "/log"):
		os.makedirs(JSMINPATH + "/log")
	else:
		shutil.rmtree(JSMINPATH + "/log")
		os.makedirs(JSMINPATH + "/log")

	logfile = open(JSMINPATH + "/log/fulllog.txt", 'w')

	logfile.write('Minify script started for js files\n')
	

	os.chdir(JSMINPATH)
	jsmincontents = glob.glob("*.js")
	logfile.write("Removing existing minified files..\n")
	logfile.write("Total "+ str(len(jsmincontents)) + " min files exist\n")
	for j in jsmincontents:
		os.remove(j)
		logfile.write("Removed file " + j + "..\n")
	os.chdir(RETVAL)
	os.chdir(JSMINPATH)
	jsmincontents = glob.glob("*.js")
	os.chdir(RETVAL)

	jscontents = os.listdir(JSDEVPATH)
	
	logfile.write("Compressing js files ")
	log_output("Compressing js files ")

	for i in jscontents:
		if i.lower().endswith('.js'):
			command = "java -jar " + YUICOMPRESSORPATH + " -v " + JSDEVPATH + "/" + i + " -o " + JSMINPATH + "/" + i[0:-3] + ".min.js 2> " + JSMINPATH + "/log/" + i[0:-3] + ".log.txt"
			#print command
			logfile.write("Compressing file "+ i + "\n")
			log_output("Compressing file "+ i + "..")
			logfile.write(command + "..\n\n")
			os.system(command)
			increment_compressed_filecount()
			increment_compressed_jfilecount()
			log_error_warning(JSMINPATH + "/log/" + i[0:-3] + ".log.txt")
	
	logfile.close()
	log_output("All js files minified")

	
def minify_css():
	if not os.path.exists(CSSMINPATH + "/log"):
		os.makedirs(CSSMINPATH + "/log")
	else:
		shutil.rmtree(CSSMINPATH + "/log")
		os.makedirs(CSSMINPATH + "/log")

	logfile = open(CSSMINPATH + "/log/fulllog.txt", 'w')
	logfile.write('Minify script started\n')

	os.chdir(CSSMINPATH)
	cssmincontents = glob.glob("*.css")
	logfile.write("Removing existing minified files..\n")
	logfile.write("Total "+ str(len(cssmincontents)) + " min files exist\n")
	for j in cssmincontents:
		os.remove(j)
		logfile.write("Removed file " + j + "..\n")
	os.chdir(RETVAL)
	os.chdir(CSSMINPATH)
	cssmincontents = glob.glob("*.css")
	os.chdir(RETVAL)

	csscontents = os.listdir(CSSDEVPATH)
	
	logfile.write("Compressing files ")

	for i in csscontents:
		if i.lower().endswith('.css'):
			command = "java -jar " + YUICOMPRESSORPATH + " -v " + CSSDEVPATH + "/" + i + " -o " + CSSMINPATH + "/" + i[0:-4] + ".min.css 2> " + CSSMINPATH + "/log/" + i[0:-4] + ".log.txt"
			#print command
			logfile.write("Compressing file "+ i + "\n")
			log_output("Compressing file "+ i + "..")
			logfile.write(command + "..\n\n")
			os.system(command)
			increment_compressed_filecount()
			increment_compressed_cfilecount()
			log_error_warning(CSSMINPATH + "/log/" + i[0:-4] + ".log.txt")

	logfile.close()

def contains(list, element):
	flag = False
	for x in list:
		if x == element:
			flag = True
	return flag

	
def minify_all():
	minify_js()
	minify_css()

def log_output(text):
	if ENABLE_LOG:
		print text

def print_summary():
	global TOTAL_FILES_COMPRESSED
	global TOTAL_JS_FILES_COMPRESSED
	global TOTAL_CSS_FILES_COMPRESSED
	print "----------------------Summary--------------------"
	print '%6s %10s' % ("Total", str(TOTAL_FILES_COMPRESSED))
	print '%6s %10s' % ("JS", str(TOTAL_JS_FILES_COMPRESSED))
	print '%6s %10s' % ("CSS", str(TOTAL_CSS_FILES_COMPRESSED))
	print "-------------------------------------------------"

parser = argparse.ArgumentParser()
group2 = parser.add_argument_group('Paths', 'describe input and output paths')

group1 = parser.add_mutually_exclusive_group()
group1.add_argument("--all", help="Minify all files", action="store_true")
group1.add_argument("--js", help="Minify all js files", action="store_true")
group1.add_argument("--css", help="Minify all css files", action="store_true")
group1.add_argument("--clear", help="Clear existing files in min", action="store_true")

group2.add_argument("--jspath", help="Path for js files")
group2.add_argument("--csspath", help="Path for css files")
group2.add_argument("--opath", help="Path for output")
args = parser.parse_args()
if args.jspath:
    if os.path.isdir(args.jspath):
        JSDEVPATH = args.jspath
    else:
        print "\033[1;31m"+ "The path specified for js is not valid"+"\033[1;m"
        exit(0)


if args.csspath:
    if os.path.isdir(args.csspath):
        CSSDEVPATH = args.csspath
    else:
        print "\033[1;31m"+ "The path specified for css is not valid"+"\033[1;m"
        exit(0)

if args.opath:
    if os.path.isdir(args.opath):
        CSSMINPATH = args.opath + '/'+CSSMINPATH
        JSMINPATH = args.opath + '/' + JSMINPATH
    else:
        print "\033[1;31m"+ "The path specified for output is not valid"+"\033[1;m"
        exit(0)

print "Minification script started" 

if args.all:
	minify_all()
elif args.js:
	minify_js()
elif args.css:
	minify_css()
elif args.clear:
	print "Clear files"

    


if not len(sys.argv) > 1 or (args.all) or (not args.js and not args.css and not args.clear):
	minify_all()

END_TIME = time.time()
print_summary()

if TOTAL_WARNINGS:
	print "Total warnings " + "\033[1;38m"+ str(TOTAL_WARNINGS)+"\033[1;m"
else:
	print "Total warnings " + str(TOTAL_WARNINGS)

if TOTAL_ERRORS:
	print "Total errors " + "\033[1;31m"+ str(TOTAL_ERRORS)+"\033[1;m"
else:
	print "Total errors " + str(TOTAL_ERRORS)

print "Time taken for execution(seconds)"
print abs(START_TIME - END_TIME)
