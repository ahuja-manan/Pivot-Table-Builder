'''
Plotting bar charts that show the highest average max temperatures
recorded in 4 major Australian cities from 1990-2012. The month and
year when that temperature was recorded are also mentioned.
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

#City names are appended to a list.
temp_city_list = []
for line in perm_data:
    temp_city_list.append(line[1])
    
city_list = list(set(temp_city_list)) 
file_name.close()

#2 lists are initialised. They will contain the maximum values
#of temperature and their corresponing year and month.
max_temp_list = []
max_month_year_list = []
for city in city_list:
    max = 0
    #the dataset is skimmed through and for every city, temperature values are checked
    #and the maximum of those values is assigned to a variable max.
    #The year and month corresponding to that max value is appended to the other list.
    for line in perm_data:
        if (city in line):
            if (float(line[3])) > max:                
                max = float(line[3])
                max_month_year = line[2] + ' ' + line[0]                
                
    max_temp_list.append(max)
    max_month_year_list.append(max_month_year)

#defining a function that saves the plotted graph as an image 
#and then prints it on an HTML page.
def webshow(img):
    savefig(img,dpi=500)
    print 'Content-Type: text/html\n'
    
    print html_start
    print '<img width="750" height="500" src="'+img+'" alt = "'+img+'"/>'
    print '<p><a href="%s">Click here to return to the input form</a></p>' % visual
    print html_end
    
N = len(city_list)
temp_val = max_temp_list
ind = arange(N)
width = 0.27
fig, ax = subplots()
ylim(20,40)


chart = ax.bar(ind+width, temp_val, width, color='r')
ax.set_ylabel('Average Max Temperature')
ax.set_title('Hottest month in Australian cities from 1990-2012')
ax.set_xticks(ind)
ax.set_xticklabels(tuple(city_list),ha='left')
index=0
for each in chart:
    height = each.get_height()
    ax.text(each.get_x()+each.get_width()/2., 1.05*height, '%s'%max_month_year_list[index],ha='center', va='top')
    index+=1
webshow("q2.png")
    



    

