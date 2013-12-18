# Minification v1
# This script generates minified version of css and js files using yui compressor.
# Declare folder paths in the script and it will generate a min folder with respective minified and log files.
#!/usr/bin/env python
import sys
import os
import glob
import shutil
import fnmatch
import os.path
import re
import argparse
import time

#Store the time the script starts
start_time = time.time()
total_files_compressed = 0
total_js_files_compressed = 0
total_css_files_compressed = 0

jsMinPath = 'min/js'
jsDevPath = 'js'
cssDevPath = 'css'
cssMinPath = 'min/css'
yuicompressorPath = 'yuicompressor.jar'

enable_log = False
retval = os.getcwd()

total_warnings = 0
total_errors = 0

print ("Minification script started") 

def logErrorWarning(filepath):
	global total_warnings
	global total_errors
	logf = open(filepath)
	warning_count = 0
	error_count = 0
	for line in logf:
		if "[ERROR]" in line:
			error_count = error_count + 1
			total_errors = total_errors + 1
		if "[WARNING]" in line:
			warning_count = warning_count + 1
			total_warnings = total_warnings + 1
	logf.close()
	logOutput("Errors " + str(error_count) + " Total Warnings " + str(warning_count))

def logOutput(text):
	print (text)

def incrementCompressedFileCount():
	global total_files_compressed
	total_files_compressed = total_files_compressed + 1

def incrementCompressedJSFileCount():
	global total_js_files_compressed
	total_js_files_compressed = total_js_files_compressed + 1

def incrementCompressedCSSFileCount():
	global total_css_files_compressed
	total_css_files_compressed = total_css_files_compressed + 1

def minifyJs():
	
	if not os.path.exists(jsMinPath + "/log"):
		os.makedirs(jsMinPath + "/log")
	else:
		shutil.rmtree(jsMinPath + "/log")
		os.makedirs(jsMinPath + "/log")

	logfile = open(jsMinPath + "/log/fulllog.txt", 'w')

	logfile.write('Minify script started for internal js files\n')
	

	os.chdir(jsMinPath)
	jsmincontents = glob.glob("*.js")
	logfile.write("Removing existing minified files..\n")
	logfile.write("Total "+ str(len(jsmincontents)) + " min files exist\n")
	for j in jsmincontents:
		os.remove(j)
		logfile.write("Removed file " + j + "..\n")
	os.chdir(retval)
	os.chdir(jsMinPath)
	jsmincontents = glob.glob("*.js")
	os.chdir(retval)

	jscontents = os.listdir(jsDevPath)
	
	logfile.write("Compressing internal js files ")
	logOutput("Compressing internal js files ")

	for i in jscontents:
		if i.lower().endswith('.js'):
			command = "java -jar " + yuicompressorPath + " -v " + jsDevPath + "/" + i + " -o " + jsMinPath + "/" + i[0:-3] + ".min.js 2> " + jsMinPath + "/log/" + i[0:-3] + ".log.txt"
			#print command
			logfile.write("Compressing file "+ i + "\n")
			logOutput("Compressing file "+ i + "..")
			logfile.write(command + "..\n\n")
			os.system(command)
			incrementCompressedFileCount()
			incrementCompressedJSFileCount()
			logErrorWarning(jsMinPath + "/log/" + i[0:-3] + ".log.txt")
	
	logfile.close()
	logOutput("All internal js files minified")

	
def minifyCss():
	if not os.path.exists(cssMinPath + "/log"):
		os.makedirs(cssMinPath + "/log")
	else:
		shutil.rmtree(cssMinPath + "/log")
		os.makedirs(cssMinPath + "/log")

	logfile = open(cssMinPath + "/log/fulllog.txt", 'w')
	logfile.write('Minify script started\n')

	os.chdir(cssMinPath)
	cssmincontents = glob.glob("*.css")
	logfile.write("Removing existing minified files..\n")
	logfile.write("Total "+ str(len(cssmincontents)) + " min files exist\n")
	for j in cssmincontents:
		os.remove(j)
		logfile.write("Removed file " + j + "..\n")
	os.chdir(retval)
	os.chdir(cssMinPath)
	cssmincontents = glob.glob("*.css")
	os.chdir(retval)

	csscontents = os.listdir(cssDevPath)
	
	logfile.write("Compressing files ")

	for i in csscontents:
		if i.lower().endswith('.css'):
			command = "java -jar " + yuicompressorPath + " -v " + cssDevPath + "/" + i + " -o " + cssMinPath + "/" + i[0:-4] + ".min.css 2> " + cssMinPath + "/log/" + i[0:-4] + ".log.txt"
			#print command
			logfile.write("Compressing file "+ i + "\n")
			logOutput("Compressing file "+ i + "..")
			logfile.write(command + "..\n\n")
			os.system(command)
			incrementCompressedFileCount()
			incrementCompressedCSSFileCount()
			logErrorWarning(cssMinPath + "/log/" + i[0:-4] + ".log.txt")

	logfile.close()

def contains(list, element):
	flag = False
	for x in list:
		if x == element:
			flag = True
	return flag

	
def minifyAll():
	minifyJs()
	minifyCss()

def logoutput(text):
	if enable_log:
		print (text)

def printsummary():
	global total_files_compressed
	global total_js_files_compressed
	global total_css_files_compressed
	print ("----------------------Summary--------------------")
	print '%6s %10s' % ("Total", str(total_files_compressed))
	print '%6s %10s' % ("JS", str(total_js_files_compressed))
	print '%6s %10s' % ("CSS", str(total_css_files_compressed))
	print ("-------------------------------------------------")

parser = argparse.ArgumentParser()
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("--all",help="Minify all files",action="store_true")
group1.add_argument("--js",help="Minify all js files",action="store_true")
group1.add_argument("--css",help="Minify all css files",action="store_true")
group1.add_argument("--clear",help="Clear existing files in min",action="store_true")
args = parser.parse_args()
if args.all:
	minifyAll()
elif args.js:
	minifyJs()
elif args.css:
	minifyCss()
elif args.clear:
	print "Clear files"


if not len(sys.argv) > 1:
	minifyAll()

end_time = time.time()
printsummary()

if total_warnings:
	print "Total warnings " + "\033[1;38m"+ str(total_warnings)+"\033[1;m"
else:
	print "Total warnings " + str(total_warnings)

if total_warnings:
	print "Total errors " + "\033[1;31m"+ str(total_errors)+"\033[1;m"
else:
	print "Total errors " + str(total_errors)

print "Time taken for execution(seconds)"
print abs(start_time - end_time)
