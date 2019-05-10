#!/usr/bin/env python
# coding: utf-8
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json

data = {}
data['jobs'] = []

base_url = "https://remote.co/remote-jobs/developer/"
response = requests.get(base_url)


base_soup = BeautifulSoup(response.text, "html.parser")
job_listings = base_soup.find_all("li", class_="job_listing")

for listing in job_listings:
	sub_url = listing.a.get("href")
	response = requests.get(sub_url)
	omi_obe = BeautifulSoup(response.text, "html.parser")

	job_div = omi_obe.div.find(class_="job_listing")

	title = job_div.h1.get_text()
	company_name = job_div.find(class_="co_name").strong.get_text()
	company_link = job_div.find(class_="links_sm").a['href']
	company_logo = job_div.img.find(class_="job_company_logo")
	apply_link = job_div.find(class_="application_button")['href']
	description = job_div.find(class_="job_description").prettify()

	data['jobs'].append(
		{
            'title': title,
			'company': company_name,
            'website': company_link,
			'logo': company_logo,
			'apply_link': apply_link,
			'description': description,
        }
	)

	time.sleep(1)
	
	
with open('remoteco.json', 'w') as data_destination:
	json.dump(data, data_destination)	
