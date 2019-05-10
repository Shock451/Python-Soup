#!/usr/bin/env python
# coding: utf-8
import requests
# to make requests to urls
import urllib.request
# for timing functions
import time
# to make use of beautiful soup library
from bs4 import BeautifulSoup
# to make use of the json library
import json

# get current time
start = time.time()

# where to store the data
data = {}

# indexing
data['jobs'] = []

# base url --- remote.co
base_url = "https://remote.co/remote-jobs/developer/"
# get the html response from the page
response = requests.get(base_url)

# Begin by creating a soup object
base_soup = BeautifulSoup(response.text, "html.parser")
# find all links to the jobs
job_listings = base_soup.find_all("li", class_="job_listing")

# for each job url
for listing in job_listings:
	# set the url
	sub_url = listing.a.get("href")
	# download the webpage 
	response = requests.get(sub_url)
	# create a soup object with the data from the webpage
	omi_obe = BeautifulSoup(response.text, "html.parser")

	# position the object at the node to start from
	job_div = omi_obe.div.find(class_="job_listing")

	# get job title
	title = job_div.h1.get_text()
	# get company name
	company_name = job_div.find(class_="co_name").strong.get_text()
	# get company link
	company_link = job_div.find(class_="links_sm").a['href']
	# get company logo
	company_logo = job_div.find(class_="job_company_logo")['src']
	# get company logo's source
	apply_link = job_div.find(class_="application_button")['href']
	# get company's location
	location = job_div.find(class_="location_sm").get_text()
	# get the time of posting from date
	post_time = job_div.find(class_="date_sm").time.get_text()
	# get the date
	date = job_div.time["datetime"]
	#get job description
	description = job_div.find(class_="job_description").prettify()
	# get tag elements
	tag_elements = job_div.find_all(class_="job_flag")
	# variable to store all tags as an array
	tags = []
	for tag_element in tag_elements:
		#loop through each tag and append its' contents
		tags.append(tag_element.get_text().strip())

	data['jobs'].append(
		{
            'title': title.strip(),
			'company': company_name.strip(),
            'website': company_link.strip(),
			'logo': company_logo.strip(),
			'apply_link': apply_link.strip(),
			'description': description.strip(),
			'tags': tags
        }
	)

	# wait a sec, don't break the site
	time.sleep(1)
	
# launch json file for external storage
with open('remoteco.json', 'w') as data_destination:
	# dump all the data extracted
	json.dump(data, data_destination)	

# store finish time
end = time.time()

# print finish time
print(end - start)