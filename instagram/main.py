from PyQt5.QtWidgets import *
from main_python import Ui_MainWindow
from settings import settings_window
from username import username_window
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pymongo
from bson.objectid import ObjectId

my_cilent=pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.smnsc.mongodb.net/test?retryWrites=true&w=majority")
url=("https://www.instagram.com/")
mydb=my_cilent["test"]
mycollection=mydb["test1"]



class main_window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.setting_object=settings_window() # setting windows object
        self.username_object=username_window()  #username_window object  
        
        self.driver=webdriver.Chrome("chromedriver.exe")
       
            

        self.ui.pb_forgot.clicked.connect(self.forgot)         
        self.ui.pb_login.clicked.connect(self.login)
        self.ui.pb_show_data.clicked.connect(self.show_me)
        self.ui.pb_search.clicked.connect(self.username_show)
        
    def forgot(self): # if push forgot password from mainwindows u wil go to this functian
        self.driver.get(f"{url}accounts/password/reset/")                 
             
    def login(self): 
                       
        self.username=self.ui.lineEdit_username.text() #take username
        self.password=self.ui.lineEdit_password.text() #take password  
        self.driver.get(url)          #get url instagram
        time.sleep(2)
        self.ui.lineEdit_username.clear()
        self.ui.lineEdit_password.clear()
        
        self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(self.username)
        self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(Keys.ENTER)  #selenium bot go to instagram 
        time.sleep(4)       
                 

        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click() #selenium bot go to instagram
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()  #selenium bot go to instagram
        
        self.driver.get(f"{url}{self.username}") # #selenium bot go to instagram username link

        self.List = {"username":self.username,"Followers":[],"Follows":[]} #List

        login_username=bool(mycollection.find_one({"username":self.username}))
        self.data()  
        self.ui.lb_info.setText("Login Success")     
        if login_username==True:
            pass
        else:
            self.followers(self.fallowers_number)

            self.driver.get(f"{url}{self.username}") # #selenium bot go to instagram username link
            time.sleep(2)
            self.follows(self.fallows_number)

            self.driver.get(f"{url}{self.username}") # #selenium bot go to instagram username link
                
            mycollection.insert_one(self.List) # add to mydb
        self.imnot_following() # take im not following data func
        self.arenot_following()   # take are not following data func 
         
    def data(self):
        time.sleep(2)      
        self.fallows_number = int(self.driver.find_elements_by_css_selector("ul.k9GMp li.Y8-fY >a.-nal3 >span.g47SY")[-1].text)
        self.fallowers_number = int(self.driver.find_elements_by_css_selector("ul.k9GMp li.Y8-fY >a.-nal3 >span.g47SY")[0].get_attribute('title'))
        self.post_number=int(self.driver.find_element_by_css_selector("ul.k9GMp >li.Y8-fY >span >span.g47SY").text)
                 
    def followers(self,max):       
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)        
        dialog = self.driver.find_element_by_css_selector("div[role='dialog'] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))        
        action = webdriver.ActionChains(self.driver)

        if followerCount==max:            
            pass
        else:
            while followerCount<max-2:                
                dialog.click()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(2)
                newCount = len(dialog.find_elements_by_css_selector("li"))
                followerCount=newCount                         
        
        followers = dialog.find_elements_by_css_selector("li") 

        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            link=link.split("/")                     
            self.List["Followers"].append(link[3])
          
    def follows(self,max):
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        time.sleep(2)
        dialog2 = self.driver.find_element_by_css_selector("div[role='dialog'] ul")
        followerCount1 = len(dialog2.find_elements_by_css_selector("li"))        

        action1 = webdriver.ActionChains(self.driver)
        if followerCount1==max:
            print(followerCount1)
            pass
        else:
            while followerCount1<max-2:                
                dialog2.click()
                action1.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(2)
                newCount2 = len(dialog2.find_elements_by_css_selector("li"))
                followerCount1=newCount2                
        follows2 = dialog2.find_elements_by_css_selector("li")        
        for user in follows2:
            link1 = user.find_element_by_css_selector("a").get_attribute("href")
            link1=link1.split("/")             
            self.List["Follows"].append(link1[3])    

    def username_fonk(self):  # username foncion    
       
       take_username=mycollection.find_one({"username":self.username_object.ui.le_search.text()}) #take find username
       self.followers_list_search=take_username["Followers"]
       self.follows_list_search=take_username["Follows"]
       self.username_object.search_username(self.followers_list_search,self.follows_list_search)
       
    def username_show(self):        
        self.username_object.show()
        self.username_object.ui.pb_okey.clicked.connect(self.username_fonk)

    def imnot_following(self):
        take_username_sd=mycollection.find_one({"username":self.username})

        self.imnot_following_list=[]
        
        for i in take_username_sd["Followers"]:

            if i in take_username_sd["Follows"]:
                pass
            else:
                self.imnot_following_list.append(i)

        self.imnotnumber=len(self.imnot_following_list)
         
    def arenot_following(self):
        take_username_sd1=mycollection.find_one({"username":self.username})

        self.arenot_following_list=[]
        
        for a in take_username_sd1["Follows"]:

            if a in take_username_sd1["Followers"]:
                pass
            else:
                self.arenot_following_list.append(a)
        
        self.arenotnumber=len(self.arenot_following_list)

    def show_me(self):      
        self.setting_object.show_data(self.fallows_number,self.fallowers_number,self.post_number,self.arenotnumber,self.imnotnumber,self.arenot_following_list,self.imnot_following_list)
              
        self.setting_object.show()
        
           

        

        
        
       


    
        

       
        
    
    
    
        
    
        

        
    

        
        
        
        
        


    
