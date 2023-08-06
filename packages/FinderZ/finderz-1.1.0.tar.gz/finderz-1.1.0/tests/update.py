import shutil
import os
#For dealing with files:

#moveFiles from one place, to the next
def moveFile(originalFileDir, newFileDir):
	shutil.move(originalFileDir, newFileDir)
	return True
def copyFile(originalFileDir, newFileDir):
	shutil.copy(originalFileDir, newFileDir)
	return True

#For dealing with directories:

#Used to move a directory:
def moveDir(originalDir, newDir):
	shutil.move(originalDir, newDir)
	return True

#Copy a directory and its contents from one place to another:
def copyDir(originalDir, newDir):
	lastdir = os.path.basename(os.path.normpath(originalDir))
	newDirectory = newDir + "/" + lastdir
	shutil.copytree(originalDir, newDirectory)
	return True

copyDir("/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/test/A/", "/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/test/B")
