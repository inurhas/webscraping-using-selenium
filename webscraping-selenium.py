##############################################################################
#
# tested on 23-27 September 2018
# Original Author: https://github.com/inurhas
# requirements: python 3.6 I was using winpython
# required python Libraries: time, random, selenimu, options and BeautifulSoup
# download google chrome webdriver on http://chromedriver.chromium.org/downloads
# extract the chrome webdriver and put the path into line 38
##############################################################################

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

src1='https://www.quora.com/topic/Lean-Startups/all_questions'
#src2='https://www.quora.com/topic/Lean-Startup-Advice-and-Strategy/all_questions'
#src3='https://www.quora.com/topic/Startup-Strategy-2/all_questions'
#src4='https://www.quora.com/topic/Small-Businesses/all_questions'
#src5='https://www.quora.com/topic/Startup-Founders-and-Entrepreneurs/all_questions'
#src6='https://www.quora.com/topic/Business-Strategy/all_questions'
#src7='https://www.quora.com/topic/Entrepreneurship/all_questions'
#src8='https://www.quora.com/topic/Innovation/all_questions'
#src9='https://www.quora.com/topic/Technology-Startups-1/all_questions'
#src10='https://www.quora.com/topic/Business-Strategy/all_questions'

#list_of_topic =[src1,src2,src3,src4,src5,src6,src7,src8,src9,src10]
list_of_topic =[src1]
#list_of_topic =["https://scrapingclub.com/exercise/list_infinite_scroll/","https://scrapingclub.com/exercise/list_infinite_scroll/"]
######################
dict_topics = {}
for idx, src_topic in enumerate(list_of_topic):
    try:
        options = Options();
        headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 Contact(irawannurhas@live.com) Aim(for-Academic-Purpose)'
        options.add_argument(f'user-agent={headers}')
        # I used google chrome
        browser = webdriver.Chrome(chrome_options=options, executable_path=r"C:\WPy-3662\webdriver\chromedriver.exe")
        
        # Tell Selenium to get the URL
        browser.get(src_topic)
        
        # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(17+(2*int(bool(random.getrandbits(1)))))
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
                        
        # Now that the page is fully scrolled, grab the source code.
        dict_topics['src'+str(idx+1)] = browser.page_source
        browser.quit()
        print('finished--'+src_topic)
    except:
        print('error skip on--src'+str(idx+1)+'--'+src_topic)
        pass

## find questions and the link example for src1
srcTopic1 = bs(dict_topics['src1'], 'html.parser')
QLtopic1 = []
for question1 in srcTopic1.findAll("a", class_="question_link", href=True, target="_blank"):
    QLtopic1.append([question1.text, question1['href']])

## find source html of each question ----------------------------------------
options = Options();
headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 Contact(irawannurhas@live.com) Aim(for-Academic-Purpose)'
options.add_argument(f'user-agent={headers}')
browser = webdriver.Chrome(options=options, executable_path=r"C:\WPy-3662\webdriver\chromedriver.exe")
browser.get("https://www.quora.com/")
time.sleep(30)
#browser.implicitly_wait(30)
#try:

for idx, question in enumerate(QLtopic1):
    totalOfLink = str(len(QLtopic1))
    print ('now is index: '+str(idx+1)+' from '+totalOfLink)
    Qlink = question[1]
    noAnswer = '/unanswered' in Qlink
    Qlink = Qlink.replace('/unanswered','')
    #Qlink ='https://www.quora.com/My-company-just-made-1-million-dollars-in-profits-Should-I-use-it-to-give-bonuses-to-my-employees-or-reinvest-it-back-into-the-business'
    # Load question page
    browser.execute_script("window.open('"+Qlink+"','new windows')")
    #browser.execute_script("window.open('https://www.quora.com/What-are-some-good-features-a-business-website-need','new windows')")
    #srcQuestion = bs(browser.page_source, 'html.parser')
    browser.switch_to.window(browser.window_handles[1])
    try:
        if noAnswer:
            TotalAns = '0 Answer'
        else:
            TotalAns = browser.find_element_by_class_name('answer_count').text
    except:
        print ('error total ans now is index: '+str(idx+1)+' from '+totalOfLink)
        TotalAns = 'NaN'
    try:    
        TotalFolw = browser.find_element_by_class_name('FollowersRow').text
    except:
        print ('error total follower now is index: '+str(idx+1)+' from '+totalOfLink)
        TotalFolw = 'NaN'
    try:    
        TotalView = browser.find_element_by_class_name('ViewsRow').text
    except:
        print ('error total view now is index: '+str(idx+1)+' from '+totalOfLink)
        TotalView = 'NaN'
    try:
        LastAsked = browser.find_element_by_class_name('AskedRow').text
    except:
        print ('error last asked now is index: '+str(idx+1)+' from '+totalOfLink)
        LastAsked = 'NaN'
    
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    if noAnswer:
        match=True
    while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    
    try:
        ListUpvotes = browser.find_elements_by_class_name('ui_button_count_optimistic_counts')
        TotalUpVote = 0
        for voteIn in ListUpvotes:
            valVote = voteIn.text.split("\n")
            if(voteIn.text==''):
                TotalUpVote = TotalUpVote + 0;
            else:
                TotalUpVote = TotalUpVote + int(valVote[0])
    except:
        print ('error total votes now is index: '+str(idx+1)+' from '+totalOfLink)
        TotalUpVote = 'NaN'
    #QLtopic1[idx].append(QLPageSrc) #save to QLtopic
    
    #find log file
    Qlog = Qlink+'/log'
    #Qlog = "https://www.quora.com/My-company-just-made-1-million-dollars-in-profits-Should-I-use-it-to-give-bonuses-to-my-employees-or-reinvest-it-back-into-the-business/log"
    browser.execute_script("window.open('"+Qlog+"','new windows')")
    browser.switch_to.window(browser.window_handles[1])
    # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    QLPageLog = browser.page_source
    try:
        logDateQuestions = browser.find_elements_by_class_name('log_action_bar')
        creationDate = logDateQuestions[-1].text
    except:
        print ('error CreationDate now is index: '+str(idx+1)+' from '+totalOfLink)
        creationDate = 'NaN'
    QLtopic1[idx].extend([TotalAns, TotalFolw, TotalView, LastAsked, TotalUpVote, creationDate])
    #QLtopic1[idx].append(QLPageLog) #save to QLtopic
print ('QLtopic1 finished')
#except:
#    print ('QLtopic1 error')
## find NaN [idx for idx,s in enumerate(QLtopic2) if "NaN" in s]
del LastAsked, ListUpvotes, QLPageLog, Qlink, Qlog, TotalAns, \
            TotalFolw, TotalUpVote, TotalView, creationDate, idx, \
            logDateQuestions, question, match, lenOfPage, lastCount, valVote

