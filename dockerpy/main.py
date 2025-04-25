#!/usr/bin/env python
# coding: utf-8

# ### SILVERSURFBOARDS WEBSCRAP - OUTLET


import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup
from jproperties import Properties


time_start = dt.datetime.now()
print(f'start time: {time_start}')

with open('/app/app.properties', 'r+b') as f:

    p = Properties()
    p.load(f,'utf-8')

# load credentials;
login = p.get('mail').data
password = p.get('password').data


# Selenium
driver = webdriver.Firefox()

url = 'https://silversurf.com.br/categoria-produto/outlet-pranchas/'

driver.get(url)


# In[ ]:


html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href = True), #{'class': "woocommerce-LoopProduct-link"})
links = links[0]


# In[9]:


# regex in the attrs href to get the ones that match 'outlet-prancha'

boards_list = []
import re

for link in links:
    
    link_text = link.attrs['href']
    match = re.search('/produto/outlet-prancha', link_text)
    if match:
        boards_list.append(link)



# lets filter with RE - get only PU and 6'0 or 6'11
boards_list_filtered = []

for board in boards_list:
    
    label = board.attrs.get('aria-label')
    if not label == None:  # this removes the secundary link (which not contains the images as children)
            
        match = re.search("6'1|6'0", label)
        
        if match:

            match2 = re.search("PU", label, re.IGNORECASE)
            if match2: 
                #and 'woocommerce-LoopProduct-link' not in board.attrs.get('class'): # we  getting 2 objs with the same purpouse - so lets get rid of one;
                
                boards_list_filtered.append(board)
    

# how its gonna be the e-mail? - Title, price and image in the body of the e-mail;

for candidate in boards_list_filtered:
    pics = []

    candidate_pics = list(candidate.children)

    try:
        candidate_pics.remove('\n')
        candidate_pics.remove(' ')
    except:
        None

    for child in candidate_pics:

        if child.attrs != {}:
    
            pics.append(f"<img src={child.get('data-lazy-src')}>")
    
    candidate['img_source'] = pics
    print(f'found {len(boards_list_filtered)} boards')

    

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


html_msg = ""

for candidate in boards_list_filtered:

    html_msg = html_msg + f"""
    <html>
        <body>
        {candidate.attrs.get('aria-label')}<br>
        link da loja: {candidate.attrs.get('href')}<br>
        images:<br>
        {''.join(candidate.attrs.get('img_source'))}
        <br>
        <br>
        <br>
        </body>
    </html>
    """


msg = MIMEMultipart("alternative")
msg['Subject'] = "Prancha em destaque"
msg['From'] = "farialimer.green@gmail.com"
msg['To'] = "farialimer.green@gmail.com"
msg.attach(MIMEText(html_msg, 'html'))

# Send email via SMTP (example with Gmail)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    
    server.login(login, password)
    server.send_message(msg)


print("Execution complete!\nMail of product's links and images are attached to the body")
print(f'End time: {dt.datetime.now()}\n')


