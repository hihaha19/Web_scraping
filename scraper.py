from bs4 import BeautifulSoup
import requests
import sys

link = 'https://www.hyperia.sk/kariera'
hyperia_link = 'https://www.hyperia.sk'

html_text = requests.get(link).content.decode('utf-8')
soup = BeautifulSoup(html_text, 'lxml')
job = soup.find_all('div', class_='offset-lg-1 col-md-10')

#more_info = hyperia_link + job.div.a['href']
#print(more_info)

for praca in job:
    title = praca.find('h3')
    print(title.text)
    more_info = hyperia_link + praca.div.a['href']
    print(more_info)