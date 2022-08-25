# Dockerfile, Image, Container
FROM python:3

ADD scraper.py .

RUN pip install requests beautifulsoup4 lxml

CMD [ "python", "./scraper.py" ]