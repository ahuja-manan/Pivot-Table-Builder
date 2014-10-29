'''
Script outputs a line graph of temperature difference vs. time 
from 2008 to 2012 with 2007 being the base year.
'''

import os,sys
os.dup2(2,3)
stderr = os.fdopen(2,'a')
stderr.close()
import matplotlib
matplotlib.use('Agg')
from pylab import *
import csv

visual = 'visualisation.html'

# html chunks
html_start = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Pivot table</title>
<link rel = "stylesheet" href = "image.css" type = "text/css" media = "screen" charset = "utf-8" />
</head>
<body><div class="container"> '''
html_end = '''
</div></body></html>'''


#the csv file is opened and the lines of
#data are appended to a permanent list called perm_data.
temp_year_list = []
temp_city_list = []
file_name = open("Dataset.csv")
data = csv.reader(file_name)
header = data.next()

perm_data = []
for line in data:
    perm_data.append(line)
    
file_name.close()


#unique list for the years and city names is created
for line in perm_data:
    temp_city_list.append(line[1])
    if line[0] > '2007':
        temp_year_list.append(line[0])      

year_list = sorted(list(set(temp_year_list))) 
city_list = list(set(temp_city_list))

#temperature values for each month in the base
#year is appended to a 2 dimensional list with
#  [temperature values of each month for city 1] etc
base_temp_2d = []
for city in city_list:
    base_temp = []
    for line in perm_data:
        if (line[0] == '2007') and (line[1] == city):
             base_temp.append(line[3])
            
    base_temp_2d.append(base_temp)

#2 dimensional list for temperature values of all the years
# of each city
#   [all temperature values for 5 years of city 1 (60 temp values)]
#   [all temperature values for 5 years of city 2 (60 temp values)] 
temp_diff_city = []
for city in city_list:
    temp_diff = []
    for year in year_list:
        for line in perm_data:
            if (line[0] == year) and (line[1] == city):
                temp_diff.append(float(line[3]))
        
    temp_diff_city.append(temp_diff)  
    
    
    

#monthly values for each year of each city subtracted to the
#respective monthly base temperature of each month of each city
#output is the new temp_diff_city list with base temp values subtracted

#loops 4 times for each city
for a in range(len(city_list)):
    
    c = 0
    #loops 5 times for each year
    for d in range(len(year_list)):
        #loops 12 times for each month
        for b in range(len(base_temp_2d[0])):
                temp_diff_city[a][c] -= float(base_temp_2d[a][b])
                c += 1

#defining a function that saves the plotted graph as an image 
#and then prints it on an HTML page.
def webshow(img):
    savefig(img,dpi=500)
    print 'Content-Type: text/html\n'
    
    print html_start
    print '<img width="1200" height="700" src="'+img+'" alt="'+img+'"/>'   
    print '<p><a href="%s">Click here to return to the input form</a></p>' % visual
    print html_end


#for loop accesses all cities and plots the temp_diff list for
#each city
for temp_diff in temp_diff_city:
    plot(temp_diff) 

legend(city_list, loc = "upper right")
xticks([w*12 for w in range(5)],['%d'%w for w in range(2008,2013)],ha='left') 
xlabel("Year", fontsize = "14")
ylabel("Temperature Difference", fontsize = "14")
title("Temperature fluctuations in Australian cities from 2008-12 w.r.t 2007.")
webshow("q3.png")    
