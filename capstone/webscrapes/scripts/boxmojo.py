import os
import datetime
import requests
import pandas as pd
from requests_html import HTML

BASE_DIR = os.path.dirname(__file__)

# open url, get html, and write to new file
def url_to_txt(url, filename="world.html", save = False):
    r = requests.get(url)
    if r.status_code ==200:
        html_text = r.text
        if save:
            with open(f"world-{year}.html",'w') as f:
                f.write(html_text)
        return html_text
    return ""


#find table you want data from
def parse_and_extract(url, name = '2021'):

    html_text = url_to_txt(url)

    r_html = HTML(html=html_text)
    table_class = '.imdb-scroll-table'
    #could also use table id below instead of class
    #table_class = "#table"
    r_table = r_html.find(table_class)
    #print(r_table)
    table_data =[]
    #check if there is text, if so pull info we want
    if len(r_table) == 1:
        # print(r_table[0].text)
        parsed_table = r_table[0]
        rows = parsed_table.find("tr") 
        header_row = rows[0]
        header_cols = header_row.find("th")
        header_names = [x.text for x in header_cols]
        
        # iterate through the rows and print
        for row in rows[1:]:
            # print(row.text)
            cols = row.find("td")
            row_data = []
            #iterate through coulmn info 
            for i, col in enumerate(cols):
                # print(i, col.text, '\n\n')
                header_name = header_names[i]
                row_data.append(col.text)
            table_data.append(row_data)
        
        #create data folder and save data to csv files    
        df = pd.DataFrame(table_data, columns = header_names)
        path = os.path.join(BASE_DIR, 'data1')
        os.makedirs(path, exist_ok = True)
        filepath = os.path.join('data1', f'{name}.csv')
        df.to_csv(filepath, index=False)
            # does the same thing as 
            # i=0
            # for x in row:
            #   i+=1
            #print(i,x)
# print(header_names)
# print(table_data)

#create function to go through the years pages
def run(start_year = None, years_ago= 44): # set start_year to none and decide how far back to go
    if start_year == None:
        now = datetime.datetime.now() #set start_year to right now
        start_year = now.year
   #set requirements: start year and years ago must be integers and have 4 integers
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}")== 4

   # go through each year from now to 1977 make a new file for each year
    for i in range(0, years_ago +1 ):
        url=f"https://www.boxofficemojo.com/year/world/{start_year}/"
        parse_and_extract(url, name= start_year)
        start_year -= 1
        #print finished when finished with each year
        print(f"finished{start_year}")

if __name__ == "__main__":
    run()



   

