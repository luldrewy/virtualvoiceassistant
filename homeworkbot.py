'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

username = "321doghot"
password = "hotdog123"

loginUrl = "https://foothillcollege.instructure.com/login"
mainUrl = "https://foothillcollege.instructure.com/"


driver = webdriver.Chrome("/Users/andrew/Downloads/chromedriver")
driver.get(loginUrl)


df = pd.DataFrame([], columns= ["title", "score"])

def getClassInfo(xpath):

    civicsClass = xpath
    civicsClass.click()
    sleep(1)

    try:
        civicsClassGrade = driver.find_element(By.XPATH, "//a[@class = 'grades']")
        civicsClassGrade.click()
        sleep(1)
    
        rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'student_assignment')]")
        
        for row in rows:
            #finds the child element of row or in other words, gets all the status "tags"
            status = row.find_element(By.XPATH, ".//td[contains(@class, 'status')]").text
            #if the status tag is missing
            if status == "MISSING":
                
                #title will get the title which is the second child element of the row 
                title = row \
                    .find_element(By.XPATH, ".//th[contains(@class, 'title')]") \
                    .find_element(By.XPATH, ".//a") \
                    .text
                score = row \
                    .find_element(By.XPATH, ".//span[contains(@class, 'tooltip')]") \
                    .text  
                
                return title, score
                
            else:
                continue
                 
    except NoSuchElementException:
        print("This class has no grades.")
    

while True:

    driver.find_element(By.NAME, "j_username").send_keys(username)
    driver.find_element(By.NAME, "j_password").send_keys(password)
    driver.find_element(By.NAME, "_eventId_proceed").click()

    #NOTE: There are two ways of checking to see if I have missing assignements:
    # 1. I can either have the bot scroll up until it reaches the end to check the list of all assignments
    # OR 2. I can have the bot click through each class and check the grades part and see if there are any assignments missing


    #Method 2 The bot clicks through each class...
    menuButton = driver.find_elements(By.CLASS_NAME, "ic-app-header__menu-list-link")
    menuButton[2].click()
    sleep(1)
    print("selected menu button")
    listOfTitles = []
    listOfScores = []
    listOfClasses = driver.find_elements(By.XPATH, ".//li[contains(@class, 'fOyUs_bGBk jpyTq_bGBk jpyTq_ycrn jpyTq_bCcs')]")
    for i in range(len(listOfClasses)):
        title = driver.find_elements(By.XPATH, ".//li[contains(@class, 'fOyUs_bGBk jpyTq_bGBk jpyTq_ycrn jpyTq_bCcs')]")[i]
        try:
            eachTitle = title.find_element(By.XPATH, ".//a")
            print(eachTitle.text)
            try:
                assignmentTitle, score = getClassInfo(eachTitle)
                
            except TypeError:
                pass
            listOfTitles += assignmentTitle
            listOfScores += score
            sleep(2)
            menuButton = driver.find_elements(By.CLASS_NAME, "ic-app-header__menu-list-link")
            menuButton[2].click()
            sleep(1)
        except NoSuchElementException:
            print("End")
            break
    assignmentData = {"assignment name" : [listOfTitles],
                        "Score " : [listOfScores]}        
    
    df = pd.DataFrame(assignmentData)
    print(df)    

    
    
  
    '''

#Get data using requests... Advantages: speed, Disadvantages: requires maintenance in the cookies
import requests
from bs4 import BeautifulSoup
import re

class_ids = {"English Junior Year": 18517, "Community": 21748, "Civics and Econs": 21740, "Philosophy and Literature": 21746}
cookies = dict(log_session_id="insert the log session id",
               canvas_session = "insert the canvas_session")

#find the pattern to get all the missing assignments
patt = re.compile(r"""<a href=\".*\">([0-9a-zA-Z\W]+)<\/a>[\s]*<div class=\"context\">([0-9a-zA-Z\W]+)<\/div>[\s]*<\/th>[\s]*<td class=\"due\">[\s]*([0-9a-zA-Z\W]+)[\s]*<\/td>[\s]*<td class=\"status\" scope=\"row\">[\s]*<span class=\"submission-missing-pill\"><\/span>""")

#start a new txt file
with open("missingAssignments.txt", "w") as f:
    f.truncate(0)
    f.write("Missing Assignments:\n")


def getAssignments():
    for subject, id in class_ids.items():
        print(subject, ": ")
        res = requests.get(f"https://foothillcollege.instructure.com/courses/{id}/grades", cookies=cookies)
        
        matches = patt.findall(res.text) #gets all the missing assignments 
        for m in matches: #for each assignment...
            name = m[0] #get the name of the assignment and write it in the file
            #print(name)
            with open("missingAssignments.txt", "a") as f: 
                f.write(name + "\n")


