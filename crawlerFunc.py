# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:00:08 2022

@author: Troy
"""
from bs4 import BeautifulSoup

def cleanURL(link,inbound,protocol,url):
    if link is not None:  
        link = link.split("#")[0]
        if (link[-1:] == "/"): #if it ends in a slash, remove it
           link = link[:-1] 
        if link[:2] == "//": #if url starts w/ 2 slashes, add HTTP or HTTPS
            link = protocol + ":" + link
        if (link[:1] == "/") : #if starts with one slash, its a relative link
            link = (url + link[1:])
        return link
                    
def AddToCrawlList(domain,link,crawllist,code,inbound):    
    if (domain[3:] in link): #check if link is within the domain
        if not any(link in crawlRow for crawlRow in crawllist): #if the link is unique
            writeOut(link,code,inbound)

def writeOut(url,code,inbound,writer,crawllist):
    crawllist.append([url,inbound]) 
    writer.write(url + ", " + str(code) + ", "+ inbound + "\n")
          
def Crawl(response,crawllist,x,writer,link):
    if response.status_code < 400 :
        data = response.text
        code = response.status_code
        soup = BeautifulSoup(data, 'lxml')
        tags = soup.find_all('a')
        imgs = soup.findAll('img')
        return (code,tags,imgs)
    else:
        writer.write(link + ", " + str(response.status_code) + ", "+ str(crawllist[x][1]) + "\n")