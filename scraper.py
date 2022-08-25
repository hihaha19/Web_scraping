import requests
import json
from bs4 import BeautifulSoup


# kontroluje, ci string poslany do funkcie je prazdny alebo nie
def empty_string(string):
    if string != "":
        return 0
    else:
        return 1

def scraper():
    link = 'https://www.hyperia.sk/kariera'
    hyperia_link = 'https://www.hyperia.sk'

    # exception, ktora riesi vsetky pripady
    try:
        html_text = requests.get(link).content.decode('utf-8')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='offset-lg-1 col-md-10')      # získam všetky div s týmto názvom na stranke
    records = []

    for job in jobs:
        title = job.find('h3')          # z kazdeho div chcem ziskat nadpis h3 na stranke https://www.hyperia.sk/kariera
        record = {
            "title": title.text
        }
        link_more_info = hyperia_link + job.div.a['href']   # vytvorim link s podrobnostami o pracovnej ponuke

        try:
            text_more_info = requests.get(link_more_info).content.decode('utf-8')   #
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        soup = BeautifulSoup(text_more_info, 'lxml')

        informations = soup.findAll('div', class_='col-md-4 icon')
        info = ""                       # do stringu info ukladam informacie o pracovnej ponuke z br tagov
        for information in informations:
            if "Miesto výkonu práce" in information.p.text:
                for br in information.p.find_all('br'):
                    text = br.next_sibling
                    info += text        # ak sa pri Mieste vykonu prace nachadza viac br tagov s
                                        # informaciami, ulozia sa vsetky do stringu 'info'

                if not empty_string(info):  # ak sa v premennej 'info' nachadza nejaka informacia, ulozi sa do slovnika
                    record["place"] = info
                else:
                    record["place"] = "Nie je uvedene"

            if "Plat" in information.p.text:
                info = ""
                for br in information.p.find_all('br'):
                    text = br.next_sibling
                    info += text

                if not empty_string(info):
                    record["salary"] = info
                else:
                    record["salary"] = "Nie je uvedene"

            if "Typ" in information.p.text:
                info = ""
                for br in information.p.find_all('br'):
                    text = br.next_sibling
                    info += text

                if not empty_string(info):
                    record["contract_type"] = info
                else:
                    record["contract_type"] = "Nie je uvedene"


        # získanie emailu
        contact = soup.find('div', class_= 'container position-contact')
        email = contact.strong
        if not empty_string(email):
            record["contact_email"] = email.text
        else:
            record["contact_email"] = "Nie je uvedeny"

        records.append(record)

    json_object = json.dumps(records, ensure_ascii=False, indent=4)
    print(json_object)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


scraper()