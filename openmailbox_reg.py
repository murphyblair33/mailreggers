#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from faker import Factory
import sqlite3

DBFILE="/home/wolfman/Documents/backup/Documents/mail_reged.db"

ff=Factory.create("En_us")
br=webdriver.Firefox()
br.get("https://www.openmailbox.org/#register")
nm=ff.name()
un=ff.user_name()
psw=ff.password()
print un
print psw
br.find_element_by_id("nom").send_keys(nm)
br.find_element_by_id("email").send_keys(un)
br.find_element_by_id("password").send_keys(psw)
br.find_element_by_id("passwordv").send_keys(psw)
with sqlite3.connect(DBFILE) as con:
    cur=con.cursor()
    cur.execute("INSERT INTO users (name,mail,passwd) VALUES ('%s','%s','%s')"%(nm,un+"@openmailbox.org",psw))
    con.commit()
    print "Added to reged DB: %s:%s"%(un+"@openmailbox.org",psw)
