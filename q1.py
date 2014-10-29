'''
Plotting the annual Melbourne rainfall over the 
last 23 years.
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
file_name = open("Dataset.csv")
data = csv.reader(file_name)
header = data.next()
perm_data = []
for line in data:
    perm_data.append(line)   
file_name.close()

#non duplicate values of year are appended
#to a list.
temp_year_list = []
for line in perm_data:
    temp_year_list.append(line[0])
    
year_list = sorted(list(set(temp_year_list)))
file_name.close()

#Yearly values of Melbourne rainfall are appended to
#a list called rainfall_list.
rainfall_list =[]
 
for year in year_list:
    rain = 0
    for line in perm_data:
        if (year in line) and ('Melbourne' in line):
            rain += float(line[4])
    
    rainfall_list.append(round((rain/12),1)) 

#defining a function that saves the plotted graph as an image 
#and then prints it on an HTML page.
def webshow(img):
    savefig(img,dpi=500)
    print 'Content-Type: text/html\n'
    
    print html_start
    print '<img width="750" height="500" src="'+img+'" alt ="'+img+'"/>'   
    print '<p><a href="%s">Click here to return to the input form</a></p>' % visual
    print html_end

#plotting the values in the rainfall list using the plot function 
#from the matplotlib library.
clf()
ylim(20,75)
plot(rainfall_list)
xticks(arange(23),year_list,rotation=90,ha='left')
ylabel("Rainfall(mm)")
title("Annual Melbourne rainfall over the past 23 years")
webshow("q1.png")  
