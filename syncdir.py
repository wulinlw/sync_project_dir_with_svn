# -*- coding: utf-8 -*-
 
u"""
同步两个文件夹
 
用法：
 
python syncdir.py source_dir target_dir
source_dir 最后不要斜杠
"""
 
import os
import sys
import shutil
import re

disableDir = ['.svn', '.settings', 'config', 'svn', 'runtime']
disableFile = ['.buildpath', '.project']

def compareFile(f1, f2):
	'''
	f1 源文件绝对路径
	f2 目的文件绝对路径
	相同True 不同False
	'''
	#check file exist
	f1Exist = os.path.exists(f1)
	f2Exist = os.path.exists(f2)
	if (f1Exist and f2Exist) != True :
		#print("file not exist:")
		#print(f1, f1Exist)
		#print(f2, f2Exist)
		return False
	fp1 = open(f1, encoding='utf-8', errors='ignore')
	fp2 = open(f2, encoding='utf-8', errors='ignore')
	try:
		lines1 = fp1.readlines()
		lines2 = fp2.readlines()
		for i,oneline in enumerate(lines1):
			pattern = re.compile(r"@version")#忽略svn版本信息的那一行
			if pattern.search(oneline):
				#print(i, oneline)
				del lines1[i]
				del lines2[i]
				break
		if lines1 == lines2:
			return True
		else:
			return False
	finally:
		fp1.close()
		fp2.close()

def main(source_dir, target_dir):
	global disableDir,disableFile
	print("synchronize '%s' >> '%s'..." % (source_dir, target_dir))
	print("=" * 50)
	sync_file_count = 0

	for root, dirs, files in os.walk(source_dir):
		relative_path = root.replace(source_dir, "")
		#print(root,dirs,files,relative_path)
		firstDirName = relative_path.split("\\")
		#print([val for val in firstDirName if val in disableDir])#list交集 
		if [val for val in firstDirName if val in disableDir] != []:
			continue
		if len(relative_path) > 0 and relative_path[0] in ("/", "\\"):
			relative_path = relative_path[1:]
		dist_path = os.path.join(target_dir, relative_path)
		#print(dist_path)

		if os.path.isdir(dist_path) == False:
			os.makedirs(dist_path)

		for filename in files:
			if filename in disableFile:
				continue
			source_file_path = os.path.join(root, filename)
			target_file_path = os.path.join(target_dir, relative_path, filename)
			#print(source_file_path,target_file_path)
			if compareFile(source_file_path, target_file_path) == False:
				shutil.copy2(source_file_path, target_file_path)
				sync_file_count += 1
				print(target_file_path)
				pass

	if sync_file_count > 0:
		print("-" * 50)
	print("%d files synchronized!" % sync_file_count)
	print("done!")
	
 
if __name__ == "__main__":
	
	if len(sys.argv) != 3:
		if "-h" in sys.argv or "--help" in sys.argv:
			print(__doc__)
			sys.exit(1)
		print(u"invalid arguments!")
	source_dir, target_dir = sys.argv[1:]
	
	if os.path.isdir(source_dir) == False:
		print(u"'%s' is not a folder!" % source_dir)
	elif os.path.isdir(target_dir) == False:
		print(u"'%s' is not a folder!" % target_dir)
 
	main(source_dir, target_dir)
