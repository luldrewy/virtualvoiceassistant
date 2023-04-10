from bs4 import BeautifulSoup
import requests
from num2words import num2words
import datetime

url = "https://weather.com/weather/tenday/l/Mountain+View+CA?canonicalCityId=b88815b210b198d188e65b9be5aec24162a749d36f4fb6eb36324666e71f1ad0"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

week = soup.find(class_ = "DailyForecast--DisclosureList--nosQS")
days = week.find_all(class_ = "DaypartDetails--Content--2Yg3_ DaypartDetails--contentGrid--2_szQ")

#the list loop is getting each day of all the days on the website. 
# And then for each day, it will find the element and get its date 
#date_text will return a list of all the dates
date_text = [day.find(class_ = "DailyContent--daypartDate--3VGlz").get_text() for day in days]
temp_text = [day.find(class_ = "DailyContent--temp--1s3a7").get_text() for day in days]
short_desc = [day.find(class_ = "DailyContent--narrative--3Ti6_").get_text() for day in days]

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]

def userDate(text):
    text = text.lower()
    

    badInput = ["nice" if month in text or day in text or (day_ext in text and digit.isdigit()) or "today" in text else "bad input" for month in MONTHS for day in DAYS for day_ext in DAY_EXTENSIONS for digit in text] 
    if "nice" in badInput:
        pass
    else:
        print("bad input")
        return "bad input"

    today = datetime.date.today()

    if "today" in text:
        return "0"
    
    # set the variables to -1 so we assume the person has not mentioned any date, day of the week, and month
    # but we will assume the year the person is referring to is this current year
    day = -1 
    day_of_the_week = -1
    month = -1
    year = today.year
    try:
        for word in text.split(): #if I say "What's the weather in August 3rd, the sentence will split and examine each word
            if word in MONTHS:    #if the word August is in the Months list which it is... 
                month = MONTHS.index(word) + 1 #the month variable will be set to the index of that month which is 7 
                                                #and then plus 1 will be 8 because python index starts at 0
            elif word in DAYS:
                day_of_the_week = DAYS.index(word)
                
            elif word.isdigit(): #if I say "August 3", the program will get 3 and see if it is a digit
                day = int(word) #because it is a digit, the day will be set to 3.
            else:
                for ext in DAY_EXTENSIONS: #for each extension in the list, Day_Extension...
                    found = word.find(ext) #the new variable found will be the index of where the extension is in the word
                                            #ie. If I say August 3rd, the found variable will be 8 because "rd" will be
                                            #in the 8th index of "August 3rd"

                    if found > 0: #if there is an extension in the word (in this case there is for August 3rd)...
                        try:

                            day = int(word[:found])
                            
                                                    #the day will be the entire string up until it reaches where the 
                                                    #extension is. In this case the string word will go up until the 
                                                    #8th index because found is equal to 8. Then we turn word to int, so 
                                                    #it becomes the day
                                                    #now variable day will become 3 because it got rid of "rd"                
                        except:
                            pass
        
        if month < today.month and month != -1: #the month I say has already passed and I specify a month (month != 0 means I spoke a month)
            year = year + 1 #then that means I am referring to next year, so we add year by 1

        if day < today.day and month == -1 and day != -1: #the day I say has already passed and I say a month and day...(If today is Feb. 26 and I say March 5th...)
            month = today.month + 1 #I will add the month by 1 because I am referring to the next month

        if day > today.day and month == -1 and day != -1: #the day I say is greater than today but I don't say a month, which means I am referring to this month
            month = today.month                         #ie. (If I say the 3rd and today is the 1st of August, I am implying August 3rd)

        if month == -1 and day == -1 and day_of_the_week != -1: #If I don't say the date and month, but only say the day of the week...
            current_day_of_week = today.weekday() #the current day of the week will be set to today (ie. Thursday)
            diff = day_of_the_week - current_day_of_week #the difference variable will measure how far today is from the day I refered
                                                        # (If I say Thursday and today is Monday, then the difference variable will be 3)
            #print(diff)
            if diff < 0: #if the difference is negative, this will mean that I am referring to next week because the day already has passed
                        # ie.(Today is Wednesday and I mention Tuesday but Tuesday already has passed, so we go to next Tuesday)
                diff += 7 #the difference variable will be seven days, in other words, we are seven days from the day we mentioned
            else:
                if "next" in text: #If I say "next" aloud, then it means I want to check next week...
                    diff += 7 #We will add 7 to the difference variable to show that we are seven days away
                        #ie.(If I say next Wednesday and today is Monday) the diff variable will be 3 first and then it will
                        # add itself by 7 which becomes 10. Next wednesday is 10 days away from today.
            
            #return today + datetime.timedelta(diff) #Return today's date added with the difference variable which is the 
                                                    #time until the specified date. If I say next Wednesday and today is Monday,
                                                    #then this command returns the current date added with 10 because there are 
                                                    #ten days until Wednesday

            diff = str(diff)
            return diff
        
        #return datetime.date(month=month, day = day, year = year) #Returns the date, not necessarily today, but the date I specified
        final_date_delta = datetime.date(month=month, day = day, year = year) - today
        final_date_delta = str(final_date_delta)
        
        return final_date_delta
    except:
        pass
        #return "bad input"



def getDate(date):
    if date == "bad input":
        return "Please specify the day"
    date_in_int = ""
    iteration = 0
    for digits in date:
        iteration += 1
        if digits.isdigit() and iteration < 3:
           date_in_int = date_in_int + digits

    date_in_int = int(date_in_int)

    date_text = [day.find(class_ = "DailyContent--daypartDate--3VGlz").get_text() for day in days]
    temp_text = [day.find(class_ = "DailyContent--temp--1s3a7").get_text() for day in days]
    short_desc = [day.find(class_ = "DailyContent--narrative--3Ti6_").get_text() for day in days]

    dict_of_days = {"Sun": "Sunday", "Mon": "Monday", "Tue": "Tuesday", "Wed":"Wednesday", "Thu":"Thursday", "Fri":"Friday", "Sat":"Saturday"}
    try:
        newDate = date_text[date_in_int] #date_text is a list, so date_in_int is the input to get a specific date we want: 0 is today and 10 is ten days from now
        newTemp = temp_text[date_in_int]
        newShortDesc = short_desc[date_in_int]
        no_digits = ""
        digits = ""
        for i in newDate: #this loop will return the string without the date ie. "Tue 07" will turn into "Tue"
            if not i.isdigit() and not i == " ":
                no_digits = no_digits + i
        
        for i in newDate: #this will get the date and store the date into the variable digits ie. "Tue 07" will become "07"
            if i.isdigit():
                digits = digits + i
        
        dateSuffix = num2words(digits, to = "ordinal")
        finalDate = dict_of_days[no_digits]
        print(finalDate + " the " + dateSuffix)
        print(newTemp + " degrees. " + newShortDesc)
        return finalDate + " the " + dateSuffix + newTemp + newShortDesc
    
    except IndexError:
        print("Date out of range")
        return "Date out of range"




