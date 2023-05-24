import json
import datetime
from random import randint
import PyPDF2 # pip install PyPDF2

currTime = datetime.datetime.now()

with open('viewed.json', 'r+') as file:
	data = json.load(file)
	visited = data["viewed"]

questions = []
revisited = len(visited) != 0

if revisited:
	prevPaper = visited[-1]
	latestDate = datetime.datetime.strptime(prevPaper['date'], "%d/%m/%y")

	dayDiff = (currTime-latestDate).days

	print(f'You last revisited on {prevPaper["date"]}, which is {dayDiff if dayDiff >= 0 else 0} day(s) ago')

	for i in visited:
		questions.append(i['page'])
else:
	print('You have never re-visited')

def doPage():
	if 'y' in input('Are you ready to do another page? ').lower():
		with open('Full_Paper.pdf', 'rb') as file:
			paper = PyPDF2.PdfFileReader(file)
			paperLen = paper.numPages

			paperSelection = randint(1, paperLen)

			if len(questions) >= paperLen:
				print("It appears you have already visited/viewed all pages, now choosing random")
			else:
				while paperSelection in questions:
					paperSelection = randint(1, paperLen)

			merger = PyPDF2.PdfMerger()

			merger.append(fileobj=file, pages=((paperSelection-1 if paperSelection-1 >= 0 else 0),paperSelection))

			output = open('currentPage.pdf', 'wb')
			merger.write(output)

			merger.close()
			output.close()

		with open('viewed.json', 'r+') as saveData:
			data = json.load(saveData)

			data['viewed'].append({
				"page": paperSelection,
				"date": currTime.strftime("%d/%m/%y"),
				"completed": False
			})

			saveData.seek(0)
			json.dump(data, saveData, indent='\t')
			saveData.truncate()
		
		print(f"Selected page {paperSelection}, written to file")

if revisited:
	if not prevPaper["completed"]:
		with open('viewed.json', 'r+') as saveData:
			data = json.load(saveData)

			data['viewed'][-1]["completed"] = 'y' in input("Have you completed your previous task? ").lower()

			saveData.seek(0)
			json.dump(data, saveData, indent='\t')
			saveData.truncate()
		
		if data['viewed'][-1]["completed"]:
			doPage()
	else:
		doPage()			
else:
	doPage()