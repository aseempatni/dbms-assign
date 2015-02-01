import sys
import requests
import lxml.html
import pprint
import numpy as np

# This script scraps the data from the imdb web pages

#sudo pip install requests==1.2.3 lxml==3.2.1

def getMovie(id):
    hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + id).content)
    movie = {}

    movie['MID'] = id

    try:
        movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
    except IndexError:
        movie['title']
    try:
        movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
    except IndexError:
        try:
            movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
        except IndexError:
            movie['year'] = ""
    try:
        movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
    except IndexError:
        movie['rating'] = ""
    try:
        movie['num_votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
    except IndexError:
        movie['votes'] = ""

    try:
        movie['genre'] = hxs.xpath('//*[@itemprop="genre"]/a/text()')
    except IndexError:
        movie['genre'] = []
    try:
        movie['country'] = hxs.xpath('//*[@id="titleDetails"]/div/h4[contains(text(),"Country")]/ancestor::div[1]/a/text()')
    except IndexError:
        movie['country'] = ""
    try:
        movie['language'] = hxs.xpath('//*[@id="titleDetails"]/div/h4[contains(text(),"Language")]/ancestor::div[1]/a/text()')
    except IndexError:
        movie['language'] = ""
    try:
        movie['location'] = hxs.xpath('//*[@id="titleDetails"]/div/h4[contains(text(),"Location")]/ancestor::div[1]/a/text()')
    except IndexError:
        movie['location'] = ""

    # try:
    #     movie['certification'] = hxs.xpath('//*[@itemprop="contentRating"]/text()')[0].strip()
    # except IndexError:
    #     movie['certification'] = ""
    # try:
    #     movie['running_time'] = hxs.xpath('//*[@itemprop="duration"]/text()')[0].strip()
    # except IndexError:
    #     movie['running_time'] = ""
    # try:
    #     movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
    # except IndexError:
    #     try:
    #         movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
    #     except Exception:
    #         movie['release_date'] = ""
    # try:
    #     movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
    # except IndexError:
    #     movie['metascore'] = 0
    # try:
    #     movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
    # except IndexError:
    #     movie['description'] = ""
    try:
        movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
    except IndexError:
        movie['director'] = ""
    try:
        movie['DID'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/@href')[0].strip()[6:15]
    except IndexError:
        movie['DID'] = ""
    # try:
    #     movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
    # except IndexError:
    #     movie['stars'] = ""
    # try:
    #     movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
    # except IndexError:
    #     movie['poster'] = ""
    # try:
    #     movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
    # except IndexError:
    #     movie['gallery'] = ""
    # try:
    #     movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
    # except IndexError:
    #     movie['storyline'] = ""

    return add_cast_details(movie,id)

    
def add_cast_details (movie,id):
    hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + id + "/fullcredits").content)

    # cast
    try:
        movie['cast'] = hxs.xpath('//*[@itemprop="actor"]/a/span/text()')
    except IndexError:
        movie['cast'] = ""    
    try:
        cast_id = hxs.xpath('//*[@itemprop="actor"]/a/@href')
    except IndexError:
        cast_id = ""
    for i in range(len(cast_id)):
        cast_id[i] = cast_id[i][6:15]
    cast =  np.column_stack([cast_id, movie['cast']])
    movie['cast'] = cast

    # producer
    try:
        movie['producer'] = hxs.xpath('//*[@id="fullcredits_content"]/table[4]/tbody[1]/tr/td[1]/a/text()')
        producer_id = hxs.xpath('//*[@id="fullcredits_content"]/table[4]/tbody[1]/tr/td[1]/a/@href')
    except IndexError:
        movie['producer'] = ""   
    for i in range(len(producer_id)):
        producer_id[i] = producer_id[i][6:15]
        movie['producer'][i] = movie['producer'][i].strip()
    # print movie["producer"]
    producer = np.column_stack([producer_id,movie["producer"]])
    movie["producer"] = producer

    return movie


def getDob(id):
    hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/name/" + id).content)
    try:
        date = hxs.xpath('//*[@itemprop="birthDate"]/@datetime')[0]
    except IndexError:
        date = ""
    return date


if __name__ == "__main__":
        id = sys.argv[1]
        data = getMovie(id)
        pprint.pprint (data)

