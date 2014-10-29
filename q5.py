'''
Monthly rainfall values averaged over a period of 23 years
and displayed on a pie chart to show the proportion of
rainfall each month for different cities.

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
</head>
<body><div class="container"> '''
html_end = '''
</div></body></html>'''


visual = 'visualisation.html'
file_name = open("Dataset.csv")
data = csv.reader(file_name)
header = data.next()

perm_data = []
for line in data:
    perm_data.append(line)
    
file_name.close()
    
temp_month_list = []
temp_city_list = []

#unique list for the months and city names created.  
for line in perm_data:
    temp_month_list.append(line[2])
    temp_city_list.append(line[1])      

month_list = sorted(list(set(temp_month_list))) 
city_list = list(set(temp_city_list)) 
    

#rainfall of each month averaged over 23 years
#displayed in 2-dimensional list rainfall
#with respect to the city
rainfall = []
for city in city_list:
    rainfall_city = []
    for month in month_list:
        rain = 0 
        for line in perm_data:
            if (city in line) and (month in line):
                rain += float(line[4])
        rainfall_city.append(rain/23)
                
    rainfall.append(rainfall_city)

#rainfall data of each month added together
#(to later get the percentage when making the pie graph)
#total_list is 2-dimensional with total rainfall of all cities
total_list =[]
for city in rainfall:
    total_rain = 0
    for a in range(len(city)):
        total_rain += city[a]
           
    total_list.append(total_rain)

#percentage of rainfall for each month
#    obtained to be plotted on the pie chart
for a in range(len(rainfall)):
    for b in range(len(rainfall[0])):
        rainfall[a][b] = (rainfall[a][b]/total_list[a]) * 100.0
        
#defining a function that saves the plotted graph as an image 
#and then prints it on an HTML page.
def webshow(img):
    savefig( img, dpi=500 )                      
    print '<img width="500" height="400" src="'+img+'"  alt ="'+img+'"/>'

    
#selects the largest percentage of each country to display seperately
def explode(rain_val_city):
    explode=[]
    for i in rain_val_city:
        if i==max(rain_val_city):
            explode.append(0.1)
        else:
            explode.append(0)
    explode=tuple(explode)
    return explode

print 'Content-Type: text/html\n'
print html_start
print '<h1>Monthly rainfall distribution in Australian cities.</h1>'
colors=['#ffff00','#9acd32','#40e0d0','#6a5acd','#87ceeb','#dda0dd','#db7093','#d3d3d3','#ffa07a','#e6e6fa','#d8bfd8','white']

clf()
pie(rainfall[0],explode=explode(rainfall[0]),labels=month_list,autopct='%1.1f%%',colors=colors)
title("%s" % city_list[0], bbox={'facecolor':'0.8', 'pad':5}) 
webshow("q5_0.png")


clf()
pie(rainfall[1],explode=explode(rainfall[1]),labels=month_list,autopct='%1.1f%%',colors=colors)
title("%s" % city_list[1], bbox={'facecolor':'0.8', 'pad':5}) 
webshow("q5_1.png") 

print '<br/>'

clf()
pie(rainfall[2],explode=explode(rainfall[2]),labels=month_list,autopct='%1.1f%%',colors=colors)
title("%s" % city_list[2], bbox={'facecolor':'0.8', 'pad':5}) 
webshow("q5_2.png")

clf()
pie(rainfall[3],explode=explode(rainfall[3]),labels=month_list,autopct='%1.1f%%',colors=colors)
title("%s" % city_list[3], bbox={'facecolor':'0.8', 'pad':5}) 
webshow("q5_3.png")
print '<p><a href="%s">Click here to return to the input form</a></p>' % visual
print html_end