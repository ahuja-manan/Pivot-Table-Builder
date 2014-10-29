import cgi

# some debugging tools, for gracefully displaying error messages
import sys
import cgitb
cgitb.enable()
sys.stderr = sys.stdout    
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

#url of the html file that creates the form
pivot_form = 'pivot_table.html'

# retrieve POST/GET user data
def get_user_input():
    form = cgi.FieldStorage()
    rows = form.getfirst("rows")
    columns = form.getfirst("columns")
    values = form.getfirst("values")
    filter = form.getfirst("filter")
    filter_value = form.getfirst("filter_value")
    return rows,columns,values,filter,filter_value


#Function that accesses data in the csv file and puts it
#into a permanent list for easy accessibility.
def get_data(filename):
    file_ = open(filename,'r')
    data = csv.reader(file_)
    header = data.next()
    
    perm_data = []
    for line in data:
        perm_data.append(line)
    file_.close()
    return perm_data

#Defining a function that gets rid of duplicate values of
#years and cities and puts them into separate lists.
def get_year_city(data):
    year_list =[]
    unique_year_list= []
    city_list = []
    unique_city_list = []
    for line in data:
        year_list.append(line[0])
        city_list.append(line[1])
    unique_year_list = sorted(list(set(year_list)))
    unique_city_list = (list(set(city_list)))
    return unique_year_list,unique_city_list

#Defining a function that creates a dictionary whose keys are 
#year, month and city and the values are lists containing their 
#non duplicate values. This is done by calling the 2 functions defined above.
#This is done for easy accessibility and also to reduce redundancy of code.
def data_dict(filename):
    data = get_data(filename)
    unique_year_list,unique_city_list = get_year_city(data)
    unique_month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    data_dict={}
    data_dict['year']= unique_year_list
    data_dict['city']= unique_city_list
    data_dict['month']=unique_month_list
    return data_dict

#check if the user input is valid and if it is not, functions are called that handle
#errors gracefully.
def get_dimensions(filename):
    d = data_dict(filename)
    rows,columns,values,filter,filter_value = get_user_input()
    #if same dimensions are selected for the table, then error is returned.
    if rows == columns:
        error_page_1()
        sys.exit()    
    for key in d:
        if rows == key:
            row_list = d[key]
        elif columns == key:
            col_list = d[key]
    #if filter is the same as rows or columns, then first it is checked if the filter values are 
    #valid or else an error is returned. If they are valid, then row_list or col_list is changed to
    #a list containing the filter values entered by the user and the number of rows or columns in the
    #to be printed table is changed accordingly.
    
    if (filter == rows) and (filter_value != "Enter filter conditions separated by commas"):
        filter_split = filter_value.split(',')
        for row_fil_val in filter_split:
            if row_fil_val not in d[rows]:
                error_page_2()
                sys.exit()
            else:
                row_list = filter_split
                
    if (filter == columns) and (filter_value != "Enter filter conditions separated by commas"):
        filter_split = filter_value.split(',') 
        for col_fil_val in filter_split:
            if col_fil_val not in d[columns]:
                error_page_2()
                sys.exit()
            else:
                col_list = filter_split
    #if there is no error, then lists containing the dimensions of the table are successfully returned.
    return row_list,col_list

#defining a function that prints an HTML page consisting of the table.
def print_pivot_table(filename):
    perm_data = get_data(filename)
    d = data_dict(filename)
    rows,columns,values,filter,filter_value = get_user_input()
    row_list,col_list = get_dimensions(filename)
    
    #if filter value(s) have been entered, then they are checked for 
    #validity or else an error is returned.
    filter_list = filter_value.split(',')
    if filter_value != "Enter filter conditions separated by commas":
        for fil_val in filter_list:
            if fil_val not in d[filter]:
                error_page_2()
                sys.exit()
    #if everything is valid and no error is returned, then the function
    #starts printing a table.    
    print '<table border="1">'
    print '<tr><td>&nbsp;</td>'
    for item_col in col_list:
        print '<th>%s</th>' % item_col
    print '</tr>'   
    
    #if filter value is still equal to the default value i.e. no filter
    #value was entered, then the list containing the whole dataset is scanned
    #and values are taken from the lines that contain both the row and column values.
    #Another point to note here is that values are summarised by average.
    if filter_value == "Enter filter conditions separated by commas":
        for item_row in row_list:
            print '<tr><th>%s</th>' % item_row 
            for item_col in col_list:
                sum = 0
                count = 0
                for line in perm_data:
                    if ((item_row in line) and (item_col in line)):
                        count += 1
                        if values == 'temp':
                            sum += float(line[3])
                        elif values == 'rain':
                            sum += float(line[4])
                    else:
                        pass 
                color_table(sum/count)
            print '</tr>'    
    #if filter value is not equal to the default value, then values
    #are taken from lines that contain the row value, column value and the 
    #the filter values. 
    #Values are again summarised by average.
    else:
        for item_row in row_list:
                print '<tr><th>%s</th>' % item_row 
                for item_col in col_list:
                    sum = 0
                    count = 0
                    for line in perm_data:
                        for val in filter_list:                     
                            if ((item_row in line) and (item_col in line) and (val in line)):
                                count += 1
                                if values == 'temp':
                                    sum += float(line[3])
                                elif values == 'rain':
                                    sum += float(line[4])
                                else:
                                    pass
                    #a function to color the cells of the table is called here.                 
                    color_table(sum/count)
                print '</tr>'
    print '</table>'
    link_to_form()
    
#defining a function to color the cells of the table. The gradual change in 
#values is shown by a gradual change in colors. Different colors are chosen 
#for different ranges of values.
#All possible ranges of values are taken care of.
def color_table(val):
    if (val) <= 15.0:
        print '<td style="background-color:#ABB2D4">%.1f</td>' % (val)  
    elif 15.0 <= (val) and (val) <= 20.0:       
        print '<td style="background-color:#969FCB">%.1f</td>' % (val)
    elif 20.0 <= (val) and (val) <= 25.0: 
        print '<td style="background-color:#727CB0">%.1f</td>' % (val) 
    elif 25.0 <= (val) and (val) <= 30.0:  
        print '<td style="background-color:#5969B6">%.1f</td>' % (val)
    elif 30.0 <= (val) and (val) <= 35.0:
        print '<td style="background-color:#485EC9">%.1f</td>' % (val) 
    elif 35.0 <= (val) and (val) <= 55.0:
        print '<td style="background-color:#5969B6">%.1f</td>' % (val)
    elif 55.0 <= (val) and (val) <= 75.0:
        print '<td style="background-color:#727CB0">%.1f</td>' % (val)
    elif 75.0 <= (val) and (val) <= 95.0:
        print '<td style="background-color:#969FCB">%.1f</td>' % (val)
    elif 95.0 <= (val) and (val) <= 115.0: 
        print '<td style="background-color:#ABB2D4">%.1f</td>' % (val)
    else:
        print '<td style="background-color:#C9D0F3">%.1f</td>' % (val)
    return None

#defining a function that deals with error of type 1 - when same values 
#are selected for rows and columns.
def error_page_1():
    print '<body>'
    print '<p> You must enter different values for Rows and Columns</p>'
    link_to_form()
    print '</body></html>'
    
#defining a function that deals with error of type 2 - when invalid filter
#values are entered.
def error_page_2():
    print '<body>'
    print '<p> You must enter valid filter values</p>'
    link_to_form()
    print '</body></html>'
    
#displaying a hyperlink that takes the user back to the original form    
def link_to_form():
    print '<p><a href="%s">Click here to return to the input form</a></p>' % pivot_form


#defining a function that calls all the neccesary functions and generates the
#HTML page.
def gen_html():
    
    print 'Content-Type: text/html\n'

    print html_start
    print_pivot_table('Dataset.csv')
    print html_end
    
#calling the gen_html function.    
gen_html()