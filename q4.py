'''
Graph obtains the scatter plot for annual temperature and rainfall data
and plots it over a period of 23 years to check the correlation
between temp and rainfall

'''
import os,sys
os.dup2(2,3)
stderr = os.fdopen(2,'a')
stderr.close()
import matplotlib
matplotlib.use('Agg')
from pylab import *
import csv

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

visual = 'visualisation.html'
file_name = open("Dataset.csv")
data = csv.reader(file_name)
header = data.next()

#the csv file is opened and the lines of
#data are appended to a permanent list called perm_data.
perm_data = []
for line in data:
    perm_data.append(line)
    
file_name.close()

#unique list for the years and city names is created    
temp_year_list = []
temp_city_list = []
for line in perm_data:
    temp_city_list.append(line[1])
    temp_year_list.append(line[0])      

year_list = sorted(list(set(temp_year_list))) 
city_list = list(set(temp_city_list))



#average annual values of temperature and rainfall
#appended to temp_list and rain_list respectively
#temp_list and rain_list contains average temp values for 
#each city over a period of 23 years (23 elements in each list) 


temp_list = []
rain_list = []
for city in city_list:
    temp_per_year = []
    rain_per_year = []
    for year in year_list:
        rain = 0
        temp = 0
        for line in perm_data:
            if (year in line) and (city in line):
                temp += float(line[3])
                rain += float(line[4])
        temp_per_year.append(temp/12)
        rain_per_year.append(rain/12)  
              
    temp_list.append(temp_per_year)
    rain_list.append(rain_per_year)   

#defining a function that saves the plotted graph as an image 
#and then prints it on an HTML page.
def webshow(img):
    savefig(img,dpi=500)
    print 'Content-Type: text/html\n'
    
    print html_start
    print '<img width="1000" height="800" src="'+img+'" alt="'+img+'"/>'   
    print '<p><a href="%s">Click here to return to the input form</a></p>' % visual
    print html_end
    
#plots temperature vs rainfall in a scatter plot    
for i in range(len(city_list)):
    plot(rain_list[i], temp_list[i], "o")        
                
legend(city_list, loc = "lower right",numpoints=1)  
xlabel("Rainfall (mm)")
ylabel("Average max temperature")
title("Relationship between Temperature and Rainfall in Australian cities")
webshow("q4.png")
