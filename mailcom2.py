#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import sqlite3,time,sys,antigate,imaplib,os,random
from PIL import Image
from faker import Factory
#from vpn_link import vpngate, geoip


DBFILE="/home/wolfman/Documents/backup/Documents/mail_reged.db"

def regit(dt):
    try:
        br=webdriver.Firefox()
        br.get("https://service.mail.com/registration.html?edition=int&lang=en&device=desktop")
        print "Firstname: %s"%dt['fname']
        br.find_element_by_css_selector("input[tabindex='1']").send_keys(dt['fname'])
        time.sleep(1)
        print "Lastname: %s"%dt['lname']
        br.find_element_by_css_selector("input[tabindex='2']").send_keys(dt['lname'])
        time.sleep(1)
        
        el={}
        [el['month'],el['day'],el['year']]=br.find_element_by_css_selector("div[class='InputText Birthday InputTextBirthday']").find_elements_by_tag_name('select')
        for op in el['month'].find_elements_by_tag_name("option"):
            if op.get_attribute("value")==str(int(dt['month'])):
                op.click()
                time.sleep(1)
        for op in el['day'].find_elements_by_tag_name("option"):
            if op.get_attribute("value")==dt['day']:
                op.click()
                time.sleep(1)
        for op in el['year'].find_elements_by_tag_name("option"):
            if op.get_attribute("value")==str(2014-int(dt['year'])):
                op.click()
                time.sleep(1)
    
        for el in br.find_elements_by_css_selector("span[class='Password']"):
            el.find_element_by_tag_name("input").send_keys(dt['pass1'])
            time.sleep(1)
        br.find_element_by_css_selector("span[class='Text EmailAddress']").find_element_by_tag_name("input").send_keys(dt['mail'].split('@')[0])
        time.sleep(1)
        br.find_element_by_css_selector("li[class='Required InputSelect SecurityQuestion']").find_element_by_class_name("Select").find_element_by_css_selector("option[value='0']").click()
        time.sleep(1)
        br.find_element_by_css_selector("li[class='Required InputText SecurityQuestionAnswer']").find_element_by_tag_name("input").send_keys(dt['city'])
        time.sleep(1)
        #cap=br.find_element_by_id("recaptcha_challenge_image")
        #cap_text=get_capt(br,cap)
        #br.find_element_by_id("recaptcha_response_field").send_keys(cap_text)        
        #br.find_element_by_css_selector("input[class='Submit']").click()
        raw_input("Press any key to close the browser...")
        br.close()
    except BaseException as err3:
        print str(err3)
        br.close()

def get_capt(br,img_element):
    location = img_element.location
    size = img_element.size
    br.save_screenshot('/tmp/fuck.png') 
    im = Image.open('/tmp/fuck.png')
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))
    im.save('captcha.png')
    a=antigate.AntiGate(key='806659243b61abd846ae7f99fa0c107c',captcha_file='captcha.png',domain='anti-captcha.com')
    time.sleep(2)
    return str(a)

def add_reged(usr):
    reged_db=DBFILE
    with sqlite3.connect(reged_db) as con1:
        cur1=con1.cursor()
        try:
            cur1.execute("CREATE TABLE users (name,mail,address,tel,birthday,passwd,city)")
            con1.commit()
        except BaseException as ee:
            print str(ee)
        cur1.execute("INSERT INTO users (name,mail,address,tel,birthday,passwd,city) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%\
        (usr["fname"]+' '+usr["lname"],usr["mail"],usr["addr"],usr["phone"],usr["year"]+'-'+usr["month"]+'-'+usr["day"],usr["pass1"],usr["city"]))
        con1.commit()
    print "Added to reged DB: "+usr["mail"]

def main():        
    #vpncsv=vpngate.get_vpncsv()
    #vpngate.get_allconfigs(vpncsv,conf_dir='/tmp/vpngate/')
    for i in range(1):
        ff=Factory.create('en_us')
        #os.system('killall openvpn;./vpngater.lnk')
        #os.system('killall openvpn')
        #random_connect('/tmp/vpngate/')
        dt={}
        dt["fname"]=ff.first_name()
        dt["lname"]=ff.last_name().replace("'","")
        dt["mail"]=ff.user_name()+str(random.randint(1,99))+'@mail.com'
        print dt["mail"]
        dt["month"]=ff.month()
        dt["year"]=str(random.randint(1970,1990))
        dt["day"]=str(random.randint(10,28))
        dt["pass1"]=dt["pass2"]=ff.password()
        print dt["pass1"]
        dt["city"]=ff.city()
        dt["phone"]=ff.phone_number()
        dt["addr"]=ff.address()
        try:
            regit(dt)
        except BaseException as err:
            print str(err)
            print "Error: "+dt["mail"]
        test_imap = raw_input("Test IMAP? ")
        if test_imap.lower()=='y':
            try:
                box=imaplib.IMAP4_SSL('imap.mail.com',993)
                print dt["mail"]+' --> '+box.login(dt["mail"],dt["pass1"])[0]
                add_reged(dt)
                print "Reged: "+dt["mail"]
            except BaseException as err:
                print str(err)
                print "Error: "+dt["mail"]
                  
if __name__ == "__main__":
    main()

