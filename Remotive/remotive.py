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

from urllib.parse import urlparse

# get current time
start = time.time()

# where to store the data
data = {}

# indexing
data['jobs'] = []

# base url --- remote.co
base_url = "https://remotive.io/jobs/software-dev"
# get the html response from the page
response = requests.get(base_url)

# Begin by creating a soup object
base_soup = BeautifulSoup(response.text, "html.parser")
# find all links to the jobs
job_listings = base_soup.find_all("li", class_="job-list-item")

# for each job url
for listing in job_listings:
	try:
		# get tag elements
		tag_elements = listing.find_all("a", class_="job-tag")
		# variable to store all tags as an array
		tags = []
		for tag_element in tag_elements:
			#loop through each tag and append its' contents
			tags.append(tag_element.get_text().strip())

		location = None
		try:
			location = listing.find("span", class_="location").span.get_text()
		except:
				location = "Remote"
		# set the url
		sub_url = listing.a.get("href")
		# download the webpage
		response = requests.get("https://remotive.io" + sub_url)
		# create a soup object with the data from the webpage
		soup = BeautifulSoup(response.text, "html.parser")

		# position the object at the node to start from
		job_div = soup.div.find(class_="job-details-page")

		# get job title
		title = job_div.h1.get_text()
		# get company name
		company_name = job_div.find(class_="company").get_text() # present
		# get website link
		website_link = "https://remotive.io" + job_div.find(class_="btn-apply")['href']
		# get company logo
		company_logo = soup.find("meta",  property="og:image")['content'] # present

		# get redirect uri
		headers = {
							"referer": "https://remotive.io" + sub_url
					}
		sub_sub_request = requests.get(website_link, headers=headers)
		# get company logo's source
		apply_link = sub_sub_request.url
		# get company link
		parsed_uri = urlparse(apply_link)
		company_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		# get job description
		description = job_div.find(class_="job-description").prettify()
		# get company's location
		date = job_div.find(class_="content").find_all("p")[1].get_text()
		# get the time of posting from date
		post_time = job_div.find(class_="content").find_all("p")[0].get_text()
		
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
	except: 
		pass


# launch json file for external storage
with open('remotive.json', 'w') as data_destination:
	# dump all the data extracted
	json.dump(data, data_destination)

# store finish time
end = time.time()

# print finish time
print(end - start)
