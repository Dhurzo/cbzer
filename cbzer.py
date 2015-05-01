# -*- coding: utf-8 -*-

import os
from pyunpack import Archive
import argparse
import shutil
import zipfile
import sys

##################
# Author: Juan Ángel López
# Licence: GNU GPL V2
##################

##### AgrsParsing####
parser = argparse.ArgumentParser(description='''Transform a CBR file into CBZ file or makes a CBZ  from JPEG files: 
Transform all CBR in the directory to CBZ files or
transform all subidirectories with JPGS in CBZ files''')
parser.add_argument("-K",'--keep',help='Keep JPEG', action='store_true')
parser.add_argument("-M",'--make',help='Make from JPEG', action='store_true')
parser.add_argument("-p",'--path',required=True,help='Path to cbr files or to JPEG files')
args = vars(parser.parse_args())
#####End AgrsParsing####

#Set target path
#Return path: Target path.
def SetPath():
	path = args['path']
	if path == '''.''':
		path = '''./'''
	return path
	
#Create temp files directories
def SetDirectory():
	try:
		if os.stat(path + cbr +'aux'):
			shutil.rmtree(path + cbr + 'aux')
			os.mkdir(path + cbr +'aux')
	except:
		os.mkdir(path+cbr+'aux')
		
#Unrar the cbr file
#Param cbr : cbr filename.
def UnrarFile(cbr):
	print '''Extacting:...''' + cbr
	Archive( path + cbr +'.cbr').extractall(path + cbr+'aux')
	
#Create cbz from subdirectory of the temp files directory.
#Param cbr : cbr filename.
#Parma myzip : zipfile descriptor
def CreateCbzFromsTempSubDir(cbr,myzip):
	subdir = [x[0] for x in os.walk(path+cbr+'aux/')]
	pics = os.listdir(str(subdir[1]))
	for pic in pics:
		myzip.write(subdir[1] +'/' + pic)
		print pic + ' added'
	print 'File closing...'
	myzip.close();
	print cbr + '.cbz has been created !!!'
	
#Create cbz from temp files directory.
#Param cbr : cbr filename.
#Parma myzip : zipfile descriptor
def CreateCbzFromsTempDir(cbr,myzip):
	pics = os.listdir(path+cbr+'aux')
	for pic in pics:
			myzip.write(path +cbr+'aux/' + pic)
			print pic + ' added'
	print 'File closing...'
	myzip.close();
	print cbr + '.cbz has been created !!!'
	
#Create a cbz file
#Param cbr : cbr filename.
def CreateCbz(cbr):
	print '''Creating cbz file...'''
	myzip = zipfile.ZipFile(path + cbr + '.cbz', 'w')
	try:
		CreateCbzFromsTempSubDir(cbr,myzip)
	except:
		CreateCbzFromsTempDir(cbr,myzip)
		
#Delete temp files and directory
#Param cbr : cbr filename.
def DeleteTempFiles(cbr):
	if not args['keep']:
		shutil.rmtree(path+cbr+'aux')
		print path+cbr+'aux deleted'
		
#List cbr files of a given path
#Param path : Target path.
#Return cbrs : List with the cbr files.
def GetPathCbrFiles(path):
	files = os.listdir(path)
	cbrs = []
	for file in files:
		if 'cbr' in file:
			cbrs.append(os.path.splitext(file)[0])
	return cbrs

#List files of a given path
#Param path : Target path.
#Return cbrs : List with the files.
def GetPathFiles(path):
	return os.listdir(path)

#List directories of a given path
#Param path : target path.
def GetPathDirs(path):
	return [x[0] for x in os.walk(path)]
	
#Make cbz file from images	
#Param subdirs: List of subdirectories with the JPEG images
def MakeCbz(subdirs):
	for subdir in subdirs[1:]:
		print 'Making cbz from ' + subdir
		myzip = zipfile.ZipFile(subdir + '.cbz', 'w')
		myzip.write(subdir)
		files = GetPathFiles(subdir)
		for file in files:
			myzip.write(os.path.join(subdir, file))
			print file + ' Inserted'
		myzip.close
		print subdir + '.cbr has been created'
		
#Show conversion errors
#Param errors: List with the cbr filenames that cause error/s
def ShowErrors(errors):
	print 'Errors:'
	for error in errors:
		print error

#MAIN:	

path = SetPath()

if not args['make']:
	errors = []
	cbrs = GetPathCbrFiles(path)
	
	for cbr in cbrs:
		try:
			SetDirectory()
			UnrarFile(cbr)
			CreateCbz(cbr)	
			DeleteTempFiles(cbr);
		except:	
			print 'Error:' + cbr + 'cannot be converted'
			DeleteTempFiles(cbr);
			errors.append(cbr);
			continue
			
	ShowErrors(errors);

else:
	
	print 'Making CBZ from images....'
	subdirs = GetPathDirs(path)
	MakeCbz(subdirs)
	

		
		
