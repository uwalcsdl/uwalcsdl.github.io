import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import os.path

baseURL = 'http://media.lcs.uwa.edu.au/echocontent/'


def getHashesFromDir(url):
	response = urllib.request.urlopen(url)
	data = response.read()
	text = data.decode('utf-8')

	links = text.split("<a href=\"")
	links = links[6:]

	hashLinks = []
	for link in links:
		hashLinks.append(link[0:36])
	return hashLinks

def checkYearWeekDay( year, week, day):
	"""Checks year, week and day ints are within valid ranges.

	Parameters
	----------
	year : int
		Two digit year abbreviation, valid range: 15 to current year
	week : int
		ISO week number, valid range: 1 to 53
	day : int
		ISO weekda, valid range: 1 (Monday) to 7(Sunday)
	lectureHash : string
		Name of lecture's parent directory (e.g. 01234567-89ab-cdef-0123-456789abcdef)

	Raises
	------
	ValueError
		If input arguments are outside of the allowed ranges
		"""
	if year < 15 or year > datetime.now().year:
		raise ValueError("Year argument out of range (valid:15-"+str(datetime.now().year)[-2:])
	if week < 1 or week > 53:
		raise ValueError("Week argument out of range (valid:1-53")
	if day < 1 or day > 7:
		raise ValueError("Day argument out of range (valid:1-7)")

class UnitXML:
	"""Class for holding the section.xml file and related info for a given unit

	Attributes
	----------
	url : string
		URL for the unit's section.xml file
	tree : ET.Element
		XML tree of unit's section.xml file
	"""

	sectionsURL = baseURL+'sections/'
	fileName = '/section.xml'

	def __init__(self, unitHash):
		self.url = self.sectionsURL+unitHash+self.fileName
		data = urllib.request.urlopen(self.url)
		data = data.read()
		self.tree = ET.fromstring(data)

	def getYear(self):
		year = self.tree.find('term').find('name')
		return year.text[2:]

	def getSem(self):
		longName = self.tree.find('name')
		if len(longName.text) < 20:
			return None
		return longName.text[-15]

	def getUnitCode(self):
		unitCode = self.tree.find('course').find('identifier')
		return unitCode.text

	def getUnitURL(self):
		unitURL = self.tree.find('portal').find('url')
		return unitURL.text

class LectureXML:
	""" class for holding the presentation.xml and related info for a given lecture

	Attributes
	----------
	url : string
		URL for the lecture's directory
	tree : ET.Element
		XML tree of lecture's presentation.xml
	"""

	fileName = 'presentation.xml'

	def __init__(self, year, week, day, lectureHash):
		""" Initialises lectureXML class by fetching presentation.xml from
		baseURL = 'http://media.lcs.uwa.edu.au/echocontent/year+week/dday/lectureHash'

		Parameters
		----------
		year : int
			Two digit year abbreviation, valid range: 15 to current year
		week : int
			ISO week number, valid range: 1 to 53
		day : int
			ISO weekda, valid range: 1 (Monday) to 7(Sunday)
		lectureHash : string
			Name of lecture's parent directory (e.g. 01234567-89ab-cdef-0123-456789abcdef)

		Raises
		------
		ValueError
			If input arguments are outside of the allowed ranges
		"""
		checkYearWeekDay( year, week, day)

		dirPath = str(year) + str(week) + '/' + str(day) + '/' + lectureHash + '/'
		self.url = baseURL + dirPath
		data = urllib.request.urlopen(self.url+'presentation.xml')
		data = data.read()
		self.tree = ET.fromstring(data)

	def getLectureUnit(self):
		unitName = self.tree.find('presentation-properties').find('name')
		unitCode = unitName.text[0:8]
		return unitCode

	def getLectureVideoURL(self):
		return self.url + 'audio-vga.m4v'

	def getLectureTime(self):
		time = self.tree.find('presentation-properties').find('start-timestamp')
		time = datetime.strptime(time.text, "%d-%b-%Y %H:%M:%S")
		time = time + timedelta(minutes=2) #Lecture recordings start 2min prior to Lecture time
		date = time.strftime("%Y-%m-%d ")
		time = time.strftime("%I%p")
		if time[0] == '0':
			time = time[1:]
		return date+time

 
def saveUnitSemesterLinks( year, semester, 
						   fileName='unitList.html', 
						   template='unitTemplate.html',
						   unitDir='units'):
	"""Fetches all units in a given semester and sets up unitCode.html files for each one.

	Parameters
	----------
	year : string
		two digit abbreviation of Year in which the units ran
	semester : string
		Semester in which the units ran
	fileName : string
		Location of HTML file to append list of units to.
	template : string
		Location of HTML template for unitCode.html files.
	unitDir : string
		Directory in which to place unitCode.html files.
	"""
	validUnit = re.compile('[a-zA-Z]{4}[0-9]{4}')
	unitHashes = getHashesFromDir(baseURL + 'sections/')
	output = []
	for i, unitHash in enumerate(unitHashes):
		xml = UnitXML(unitHash)
		if xml.getYear() == year:
			if xml.getSem() == semester:
				unitCode = xml.getUnitCode()
				if not validUnit.match(unitCode):
					continue
				unitURL = xml.getUnitURL()
				unitInfo = unitCode, unitURL
				output.append(unitInfo)
		if i%500==0:
			percent = str(i/len(unitHashes)*100)
			print( percent + "%" +" complete")
	output.sort()

	print("Fetched "+str(len(output))+" units, writing to file...")
	unitListFile = open(fileName, 'a')
	for unit in output:
		unitLine = "<li> {0}      <a href=\"{2}/{0}.html\">Download</a>     <a href=\"{1}\">View Online</a></li>".format(unit[0], unit[1],unitDir)
		unitListFile.write(unitLine)
	unitListFile.close()

	templateFile = open(template, 'r')
	template = templateFile.read()
	templateFile.close()

	for unit in output:
		unitPage = open(unitDir+'/'+unit[0]+'.html', 'w')
		unitTemplate = template.replace('{{pageTitle}}', unit[0]+' Lectures')
		unitPage.write(unitTemplate)
		unitPage.close()

def fetchDaysUnits( year, week, day):
	checkYearWeekDay(year, week, day)
	print('day '+str(day))
	lectureHashes = getHashesFromDir(baseURL+str(year)+str(week)+'/'+str(day))
	for lectureHash in lectureHashes:
		try:
			xml = LectureXML(year, week, day, lectureHash)
		except urllib.error.HTTPError:
			continue
		unitCode = xml.getLectureUnit()
		if unitHasPage(unitCode):
			lectureURL = xml.getLectureVideoURL()
			lectureDateTime = xml.getLectureTime()
			appendLecture(unitCode, lectureURL, lectureDateTime)

def unitHasPage(unitCode):
	return os.path.isfile('units/'+unitCode+'.html')

def fetchWeeksUnits( year, week):
	print('Fetching /'+str(year)+str(week))
	for day in range(1,8):
		fetchDaysUnits( year, week, day)

def addUnit(unitCode):
	pass

def appendLecture(unitCode, lectureURL, lectureDateTime):
	unitPage = open('units/'+unitCode+'.html', 'a')
	link = '<li><a download="{1} {2}.m4v" href="{0}">{2}</a></li>\n'.format(lectureURL, unitCode, lectureDateTime)
	unitPage.write(link)
	unitPage.close()