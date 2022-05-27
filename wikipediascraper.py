#import our modules or packages that we will need to scrape a website 
import csv #this is used to use functions for csv files
import time # use this library to use the time function 
from bs4 import BeautifulSoup #this is used to scrape and parse internet data
import requests 

time.sleep(2) #sleep() ②, which basically tells our scraper to take a break, this doesnt
#overload the websites severs while we scrape. 

#identification 
headers = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/65.0.3325.162 Safari/537.36",
            "from": "Joas Cerutti joascerutt@gmail.com"}#First, we can give 
            #the website owner information about the kind of user-agent ① we’re using
            #Then we can specify who we are ② within a string assigned to the key from. ②

#make an empty array 
rows = []

#open the website 
urls = ["https://en.wikipedia.org/wiki/Category:Women_computer_scientists", 
"https://en.wikipedia.org/w/index.php?title=Category:Women_computer_scientists&pagefrom=Lin%2C+Ming+C.%0AMing+C.+Lin#mw-pages"]
#The variable urls holds a list of two strings: the URL of the first Wikipedia page, 
#which holds the first half of the names of women computer scientists, 
#and then the link for the second page that holds the rest of the names

def scrape_content(url): # In here we are telling Python that we’re creating a 
    #function called scrape_content() that takes the argument url

    page = requests.get(url, headers=headers) #the variable page gets set set to contain the HTML page, which we open using 
    #the requests library's get() function. This functions grabs the site from the web. 

    page_content = page.content #Now we using the content property from requests to encode the HTML of the 
    #page we just opened and ingested the previous line as bytes that are interpretable by BeautifulSoup.

    #parse the page with Beautiful Soup Library
    soup = BeautifulSoup(page_content, "html.parser") #This helps our script differentiate between HTML
    #and the sites content.

    content = soup.find("div", class_= "mw-category-columns") # we use the find() function to find a <div> tag that contains
    #the class mw-category. This is the overall <div> tag that contains the content we want to scrape.

    all_groupings = content.find_all("div", class_="mw-category-group") #


    for grouping in all_groupings: #to go through all different groupings in the website
        names_list = grouping.find("ul")  # gathered the unordered list tag <ul> and store it in a variable 
        category = grouping.find("h3").get_text() # get all the headline <h3> tags and store in category.
        alphabetical_names = names_list.find_all("li") #
        
        #now we are going to get the data that contains the name, the link, and the letter connected to each name
        for alphabetical_name in alphabetical_names:
            #get name 
            name = alphabetical_name.text
            
            
            #get link
            anchortag = alphabetical_name.find("a", href = True)
            
            #get the link 
            link = anchortag["href"] #We want to get the link inside the anchor tag, so we need to access 
            #the tag’s href value, which is stored in the tag as an attribute. 
            #We do this by grabbing the href attribute using brackets containing the string "href"
            
            #get the letter 
            letter_name = category
            
            # make a dictionary that will be written into the csv
            row = {"name": name, #Then we proceed to assign each key (name, link, and letter_name)  
                "link": link, #the value that holds the corresponding data we gathered earlier in the script.
                "letter_name": letter_name} #In the end, we append the row of data to our list variable rows 
            
            rows.append(row)
    

for url in urls: # Then we write a for loop that cycles through every URL in our urls list 
    # and runs the scrape_content() function 
    scrape_content(url) # for each URL. If you wanted to run the scraper on more Wikipedia 
    #list pages, you would simply add those as links to the urls list.

# make a new csv into which we will write all the rows
with open("all-women-computer-scientists.csv", "w+") as csvfile: #we use the with open() as 
    #csvfile ① statement to create and open an empty .csv file called 
    #all-women-computer-scientists.csv
    
    # these are the header names:
    fieldnames = ["name", "link", "letter_name"] #② Since we’re using a dictionary to 
    #gather our data, we need to specify a list of header names for our spreadsheet
    
    # this creates your csv
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) #③ and then use the DictWriter() 
    #function from the csv library 
    
    # this writes in the first row, which are the headers
    writer.writeheader() #④ to write each header into the first row 
    
    # this loops through your rows (the array you set at the beginning and 
    # have updated throughtout)
    for row in rows: #⑤ Finally, we need to loop through each row that we 
    #compiled in the rows list ⑤ 
        # this takes each row and writes it into your csv
        writer.writerow(row) #⑥write each row into our spreadsheet 
    
    
    
