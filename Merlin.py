# Author: A. Berkay Bal
# ID: 21201318

###########################################################################################

#! /usr/bin/env python3
from perceval.backends.core.git import Git
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd

# URL for the git repo to analyze		
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																											
repo_url = 'https://github.com/microsoft/QuantumLibraries' # 25 contibutors, 65+ commits in last 3 months, active for 3+ years

# directory for letting Perceval clone the git repo
repo_dir = '/tmp/QuantumLibraries.git'

# Git object, pointing to repo_url and repo_dir for cloning
repo = Git(uri=repo_url, gitpath=repo_dir)

print("\n---------------Q3-------------------")

def monthAsInt(month):
        result=0
        if month=="Jan":        result = 1
        elif month=="Feb":        result = 2
        elif month=="Mar":        result = 3
        elif month=="Apr":        result = 4
        elif month=="May":        result = 5
        elif month=="Jun":        result = 6
        elif month=="Jul":        result = 7
        elif month=="Aug":        result = 8
        elif month=="Sep":        result = 9
        elif month=="Oct":        result = 10
        elif month=="Nov":        result = 11
        elif month=="Dec":        result = 12
        return result
               
countActivity=0
commArr = [None]

# past months
then = dt.date.today() - rd(months=10)
print("Date 10 months before: ",then,"\n")

for commit in repo.fetch():
	str = commit['data']['CommitDate']
	if str is not None:
                commArr.append(str)

                # check whether commit date is withing past 10 months
                year = int(str.split()[4])
                month = monthAsInt(str.split()[1])
                day = int(str.split()[2])
                
                # checking the condition
                if( int (( (datetime(then.year,then.month,then.day)-datetime(year, month, day)).days%365 ) / 12) <= 10 ):
                        countActivity = countActivity + 1

print("Number of commits in last 10 months: ",countActivity,"\n")


# commit longevity
year2 = int(commArr[len(commArr)-1].split()[4])
month2 = monthAsInt(commArr[len(commArr)-1].split()[1])
day2 = int(commArr[len(commArr)-1].split()[2])

year1 = int(commArr[1].split()[4])
month1 = monthAsInt(commArr[1].split()[1])
day1 = int(commArr[1].split()[2])

longevityDays = datetime(year2, month2, day2) - datetime(year1, month1, day1)
longevityFormatYear = int(longevityDays.days/365)
longevityFormatMonth = int((longevityDays.days%365)/12)
longevityFormatDay = int(((longevityDays.days%365)%12)/30)

print("First commit: ",commArr[1])
print("Last commit: ",commArr[len(commArr)-1])
print("Longevity: ", longevityDays , " or " , "Years: ",longevityFormatYear, " Months: ",longevityFormatMonth, " Days: ",longevityFormatDay,"\n")

# fetch all commits and print each author
print("\n---------------Q4-------------------")

# find size of an array
def arrLen():
        size = 0
        for commit in repo.fetch():
                size = size + 1
        return size

# find index of maximum element in an array     
def findMaxIndex(arr):
        for x in range(len(arr)):
                if arr[x]==max(arr):
                        return x
        return -1

# add committers to an array
arr = []

for commit in repo.fetch():
        x = commit['data']['Author']
        if x not in arr:
                arr.append(x)
arr.sort()

# declare occurence and commit date arrays
size = len(arr)
occ = [None] * size
date = [None] * size

# fill occurence array with initial values for commits
for x in range(size):
        occ[x] = 0

# fill occurences
for commit in repo.fetch():
        x = commit['data']['Author']
        y = 0
        if x in arr:
                for i in range(size):
                        if arr[i]==x:
                                occ[i]=occ[i]+1
# show informations
def printAllInfo():
        print("List of commiters:\n", arr)
        print("Number of commiters: ", size)
        print("Amounts of commits:\n", occ)

def printAuthorCommit(name):
        for x in range(size):
                if name == arr[x]:
                        print("Commiter: ", name)
                        print("\nCommits: ", occ[x])
                        print("\n")

def printAllInfoList():
        for x in range(size):
                print("Commiter: ", arr[x])
                print("Commits: ", occ[x])
                print()
        
        # show the information
        maxIndex = findMaxIndex(occ)
        print("--------------------\n")
        print("Max Commiter: ", arr[maxIndex])
        print("Max Commit: ", occ[maxIndex])
        print()
                
# printAllInfo() -> show all details
# printAuthorCommit(arr[index]) -> show commit information of a commiter

printAllInfoList()

print("---------------Q5-------------------")
# print column names of data
def printCommitDates():
	for commit in repo.fetch():
		for y in commit['data']:
			print(y)

#commit,refs,parents,Commit,CommitDate,files,message,Merge,Author,AuthorDate
datesArr = [None]
commitYearArr = [None]
for commit in repo.fetch():
	str = commit['data']['CommitDate']
	if str is not None:
	        #print(str)
	        if ("Jun" in str) or ("Jul" in str) or ("Aug" in str):
	                datesArr.append(str)
	                commitYearArr.append(str.split()[4]) # year
	                
# <Weekday Month Day Time Year GMT> commit format        
counter = 0
commitAmountByYear = [None]
maxYearSummer=0
maxCommitSummer=0

# ( it will not show the years if there is no commit in summer )
for x in range(len(datesArr)):
        # head is empty, condition to check commit years whether they are new
        if x>0 and x<len(datesArr)-1:
                if x==1:
                        counter = 1
                elif commitYearArr[x]==commitYearArr[x-1]:
                        counter = counter + 1
                elif commitYearArr[x]!=commitYearArr[x-1]:
                        print(commitYearArr[x-1], ":", counter, "commits")
                        commitAmountByYear.append(counter)
                        counter = 1
        # condition to check commit for last commit year whether it is new
        elif x==len(datesArr)-1:
                if commitYearArr[x]==commitYearArr[x-1]:
                        print(commitYearArr[x-1], ":", counter+1, "commits")
                        commitAmountByYear.append(counter)
                elif commitYearArr[x]!=commitYearArr[x-1]:
                        print(commitYearArr[x], ":", 1, "commits")
                        commitAmountByYear.append(counter)
        
        # find max commit amount and its year in summer commits
        if counter>maxCommitSummer:
                maxCommitSummer=counter
                maxYearSummer=commitYearArr[x-1]

# show the information ( it will not include the years if there is no commit in summer )
print("Max summer commit amount ", maxCommitSummer+1, " observed in ", maxYearSummer)  
        
   
        
