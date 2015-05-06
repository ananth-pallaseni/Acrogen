#!/usr/bin/env python

import sys

# Filename of dictionary to use when checking if a word is a valid English word
globalDictionaryFile = "GlobalDictionary.txt" 
globalDictionary = read(globalDictionaryFile)

# Filename of a list of nouns
nounsFile = 'nouns_full.txt' 
nouns = read(nounsFile)

def read(filename, whitelist='abcdefghijklmnopqrstuvwxyz '):
	""" Function to read a txt file and return a list of all the words it contains. WARNING: result may contain repeated words """
	l = []
	
	with open(filename) as f:
		# For each line in filename:
		for line in f.readlines():
			# Make the line lowercase
			lowercase = line.lower()
			# Get rid of unwanted characters
			whiteListed = enforceWhiteList(lowercase, whitelist)
			# Split it into words
			words = whiteListed.split()
			# Add the words to the list
			for w in words:
				l.append(w)

	return l

def enforceWhiteList(s, whitelist='abcdefghijklmnopqrstuvwxyz '):
	""" Enforce a whitelist upon a string s"""
	clean = ''
	for i in range(len(s)):
		if s[i] in whitelist:
			clean += s[i]
	return clean


def singles(wordlist):
	""" Removes duplicate words from a list"""
	newList = []
	for w in wordlist:
		if w not in newList:
			newList.append(w)
	return newList


def check(word, wordList=None):
	""" Checks if word is in wordlist"""
	if wordList:
		return word in wordList
	else:
		return word in globalDictionary

def corpusToDict(corpusFileName):
	""" Given a file name in txt format, return the list of potential words for this acronym""" 
	return onlyNouns(singles(read(corpusFileName)))

def dictToLetters(d):
	""" Given a list of words, return a list of the first letters in each of those words """
	firstLetters = []
	for w in d:
		c = w[0]
		if c not in firstLetters:
			firstLetters.append(c)
	return firstLetters

def lettersToAcronyms(letters, size):
	""" Given a list of first letters and the size, return all possible acronyms """
	# Object that tracks permutations of letters
	perms = Permutation(size, len(letters_2))
	word = ""
	validAcr = []

	# Go through all permutations of letters with specified size
	while perms.next():
		word = ""
		# Construct new permutation
		for i in range(size):
			index = perms[i]
			letter = letters[index]
			word += letter

		# If the new word is in the global dictionary and not already seen add it to the list
		if check(word) and word not in validAcr:
			validAcr.append(word)

	return validAcr

def mapLettersToWords(words):
	""" Given a set of words, map the letters of the alphabet to the list of words that start with that letter """
	d = {}
	for l in 'abcdefghijklmnopqrstuvwxyz':
		d[l] = []

	for w in words:
		firstLetter = w[0]
		if w not in d[firstLetter]:
			d[firstLetter].append(w)

	return d


def acronymsToMeanings(acronyms, mapping):
	"""" Given a set of acronyms and a mapping of letters to words, return a list containing potential meanings of each acronym.
		 A meaning is the assignment of a word to each letter to the acronym, eg: BART could be Bay Area Rapid Transit """

	meanings = []

	for a in acronyms:
		assignMeaning('', a, mapping, meanings)

	return meanings

def assignMeaning(stub, remaining, d, completed):
	""" Given a partially completed stub of a meanings, how much of the acronym is left, a mapping of letters to words 
		and a list to place completed meanings, this function generates all possible meanings for an acronym """
	# If there is no acronym remaining, we are done
	if remaining == '':
		completed.append(stub)
		return

	# Find the list of words for the next letter
	nextLetter = remaining[0]

	# Enumerate the possible list of words for the above letter
	choices = d[nextLetter]

	# For each of the possible words that are not already in the stub, add them to the stub and call this function again
	for c in choices:
		if c not in stub:
			newStub = stub + " " + c
			assignMeaning(newStub, remaining[1:len(remaining)], d, completed )


def acrogen(size, corpus, printVals, outputfile):
	words = corpusToDict(corpus)
	letters = dictToLetters(words)
	acronyms = lettersToAcronyms(letters, size)
	mapping = mapLettersToWords(words)
	meanings = acronymsToMeanings(acronyms, mapping)

	if printVals:
		for m in meanings:
			print(m)

	writeToFile(outputfile, meanings)

def writeToFile(filename, items):
	f = open(filename, 'w')
	for i in items:
		f.write(i + '\n')
	f.close()


def argParse(args):
	size = 0
	printVals = False
	outputfile = 'acrogenOut'
	corpus = globalDictionaryFile

	i = 1
	l = len(args)
	while i < l:
		current = args[i]
		if current == '-s':
			size = args[i+1]
			i += 2
		elif current == '-c':
			corpus = args[i+1]
			i += 2
		elif current == '-p':
			printVals = True
			i += 1
		elif current == '-o':
			outputfile = args[i + 1]
			i += 2
		else:
			i += 1

	return int(size), printVals, outputfile, corpus


class Permutation(object):
	"""A class that permutes a set of values from 0 to maxVal-1 (inclusive)"""
	def __init__(self, numVals, maxVal):
		self.numVals = numVals
		self.maxVal = maxVal
		self.vals = [0 for i in range(numVals)]
		self.vals[0] = -1
		self.done = False

	def next(self):
		if self.done:
			print("DONE")
			return False

		self.vals[0] += 1
		if self.vals[0] > self.maxVal - 1:
			self.vals[0] = 0
			i = 1
			while i < self.numVals and self.vals[i] >= self.maxVal - 1:
				self.vals[i] = 0
				i += 1
			if i < self.numVals:
				self.vals[i] += 1
			else:
				print("furthest is oob")
				self.done = True
				return False

		return self.vals
		

	def __getitem__(self, key):
		return self.vals[key]

	def __str__(self):
		return "Permutation. Current State = " + str(self.vals)

	def __repr__(self):
		return self.__str__()	


if __name__ == '__main__':
	args = sys.argv
	fnArgs = argParse(args)

	size = fnArgs[0]
	printVals = fnArgs[1]
	outputfile = fnArgs[2]
	corpus = fnArgs[3]

	acrogen(size, corpus, printVals, outputfile)


