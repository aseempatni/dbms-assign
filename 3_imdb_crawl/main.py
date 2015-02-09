import sys
import requests
import lxml.html
import pprint
import parse
import subprocess

#sudo pip install requests==1.2.3 lxml==3.2.1

# root of the site to be crawled
root = "http://www.imdb.com"

# init
initialLink = "/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc"
suf = ""

def getLinks(link):
	# get xml document
	hxs = lxml.html.document_fromstring(requests.get(link).content)

	# get list of movie ids
	try:
		links = hxs.xpath('//*[@class="title"]/a/@href')
	except IndexError:
		links = "holy shit - no links"
	
	# find next page url
	try:
		next = hxs.xpath('//*[@class="pagination"]/a[contains(text(),"Next")]/@href')
	except IndexError:
		next = "holy shit - no next page"
	
	global suf
	suf = next[0]
	return links


if __name__ == "__main__":
	no_of_pages = 2
	suf = initialLink

	#open file for config parameters
	f = open('input.txt', 'r')

	# read initial link
	link = f.readline().strip()

	for i in range(no_of_pages):

		# get list of ids from link
		print "Getting ids from " + link
		ids = getLinks(link)
		print ids

		# next link
		link = root + suf

		# parse movie data for the ids
		for id in ids:
			subprocess.call(["python","movie.py",id[7:-1]])

	print "All done :-)"

