from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import sys
import os

const_timeline , const_about , const_friends , const_photo = ['&sk=timeline','&sk=about','/friends','&sk=photos_of']
about_parms = ['&section=overview','&section=education','&section=living','&section=contact-info','&section=relationship','&section=bio','&section=year-overviews']

def log_in (browser,ID,pasword):
    browser.get("https://www.facebook.com/")
    browser.find_element_by_id("email").send_keys(ID)
    browser.find_element_by_id("pass").send_keys(pasword)
    browser.find_element_by_id("loginbutton").click()
    time.sleep(1)

def Scrol_down(browser):
    flag = True
    num = 0
    while flag:
        num +=1
        start = browser.page_source
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(0.5)
        stop = browser.page_source
        if start==stop:
            flag = False
        print("Page Updated Times :", num )

def Get_friends_info(browser,Profile_ID):
    browser.get('https://www.facebook.com/'+Profile_ID+const_friends)
    Scrol_down(browser)
    sourse = browser.page_source
    soup = BeautifulSoup(sourse,features="lxml")
    friends = soup.select('#pagelet_timeline_medley_friends')[0].find_all("li", class_= ["_698"])
    #name = friends[0].select('.fsl.fwb.fcb')[0].get_text()
    #photo = friends[0].select('img')[0].get('src')
    #profile_link = friends[0].select('.fsl.fwb.fcb a')[0].get('data-gt')
    key = ["Name","Profile_id","Photo_Link"]
    temp = []
    for i in friends:
        try:
            temp.append([i.select('.fsl.fwb.fcb')[0].get_text(),json.loads(i.select('.fsl.fwb.fcb a')[0].get('data-gt'))['engagement']['eng_tid'],i.select('img')[0].get('src')])
        except:
             pass
    temp  = json.dumps([dict(zip(key,t)) for t in temp],indent=4)
    return temp

def Get_timeline_link(browser,Profile_ID):
    browser.get('https://www.facebook.com/'+Profile_ID)
    Scrol_down()
    sourse = browser.page_source
    soup = BeautifulSoup(sourse)
    timelines = soup.select('._5pcb._4b0l._2q8l')
    temp = [i.select('a._5pcq')[0].get('href') for i in timelines if i.select('a._5pcq')!=[]]
    for i in range(len(temp)):
        if temp[i][0] == '/':
            temp[i] = 'https://www.facebook.com'+temp[i]
    return temp

def timeline_parser(browser,timeline_link):
    browser.get(timeline_link)
    try:
        browser.find_element_by_class_name('_xlt._418x').click()
    except:
        pass
    sourse = browser.page_source
    soup = BeautifulSoup(sourse)
    focus = soup.select('#contentArea')[0]
    focus_comment = soup.select("._4299")[0]
    try:
        Time_Line_Head = focus.select('.fwn.fcg')[0].get_text()
    except:
        Time_Line_Head = None
    try:
        info = focus.select(".fsm.fwn.fcg")[0].get_text()
    except:
        info = None
    try:
        message = focus.select("._5pbx.userContent._3576")[0].get_text()
    except:
        message = None
    try:
        like = focus_comment.find_all("span", class_= ["_81hb"])[0].get_text()
    except:
        like = None
    try:
        comment = focus_comment.find_all("div" ,class_=["_4vn1"])[0].get_text()
    except:
        comment = None
    try:
        Tagged =[ i.get("data-tooltip-content") for i in focus.select('.fwn.fcg')[0].find_all("a") if i.get("data-tooltip-content")!=None][0].split("\n")
        if Tagged ==[]:
            Tagged = None
    except:
        Tagged = None
    try:
        date = focus.select(".fsm.fwn.fcg")[0].select("a")[0].get_text()
    except:
        date = None
    try:
        location = focus.select(".fsm.fwn.fcg")[0].select("a")[1].get_text()
    except:
        location = None
    Poster = focus.select('.fwn.fcg')[0].select(".fwb")[0].get_text()
    comment , share = None,None
    for i in focus_comment.find_all("div" ,class_=["_4vn1"])[0].find_all("a"):
        if i.get_text()[-2:] == "留言":
            comment =  i.get_text()[:-3]
        if i.get_text()[-2:] == "分享":
            share =  i.get_text()[:-3]
    key = ['Poster' , 'Time_Line_Head' , 'date' , 'location' , 'message' , 'like' , 'comment' , 'share']
    value = [Poster , Time_Line_Head , date , location , message , like , comment , share]
    return  json.dumps(dict(zip(key,value)) , indent = 4 )

def main():
    email = input("Type Your E-mail:")
    pas = input("Type Your Password:")
    root_id = input("Type Your User_ID (make sure the ID is same as the account you login last step):")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # 啟動無頭模式
    chrome_options.add_argument('--disable-gpu') # windowsd必須加入此行
    
    browser = webdriver.Chrome("C:\\Users\\win10\\Desktop\\PROGRAM\\HACK\\chromedriver.exe",chrome_options=chrome_options)
    log_in(browser,email,pas)
    if os.path.isfile("Root_Json.json"):
        with open("Root_Json.json","r") as f:
            Friend_Json = json.loads(f.read())
    else:
        print("Creating Root Account Data (This may Take a long Time according the number of friends of your Account)")
        start_time = int(time.time())
        Friend_Json = Get_friends_info(browser,root_id)
        stop_time = int(time.time())
        with open("Root_Json.json", 'w') as f:
            f.write(Friend_Json)
        print("Done ["+str(stop_time - start_time)+' sec]')    
    print(Friend_Json)


main()