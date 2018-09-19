#python 3.6
import bs4, requests
import logging
from Media_Class import *


def Insert_Media(media_obj,media_list):
    if len(media_list)==0:
        media_list.append(media_obj)
        return media_list

    #check that the name does not appear again
    for i in media_list:
        if i.get_name()==media_obj.get_name(): #if the name already appears
            return media_list #return the list unchanged

    """if len(media_list)==1:
        if media_list[0].get_rating()<media_obj.get_rating():
            media_list.insert(0,media_obj)
            return media_list
        else:
            media_list.append(media_obj)
            return media_list"""


    #add media_obj to correct place based on rating

    #TODO: implement optimized insertion !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    added=False
    for i in range(len(media_list)):
        if media_list[i].get_rating()<media_obj.get_rating():
            media_list.insert(i,media_obj)
            added=True
            break

    if not added:
        media_list.append(media_obj)

    return media_list

def get_rating_votes(link):
    """
    extract the rating and the votes of the media from its page
    """
    while(True): #loop until the page is downloaded succesfuly
        try:
            res=requests.get(link) #request the page
            res.raise_for_status() #raise exception in case of error
            page_soup=bs4.BeautifulSoup(res.text) #create a BeautifulSoup object
            break
        except requests.exceptions.ConnectionError:
            print('connection error, retrying...')
            time.sleep(5)

    rating=float(page_soup.find("span",{"itemprop":"ratingValue"}).text)
    votes=float(page_soup.find("span",{"itemprop":"votes"}).text)

    return rating,votes

def Handle_Object(object_elm):
    """
    recieves the media object from the /browse.php page and creates a Media object
    by scraping the objects page on the site
    """
    name= object_elm.text.split('\n')[0] #extract the media name (the split removes the stuff that is not the name like publishing date and file size)
    link="http://kinozal.tv"+object_elm.find("a")['href'] #extract link to media page
    rating,votes=get_rating_votes(link) #get the rating and the votes of the media
    return Media(name,link,rating,votes) #create Media object and return it

def main(media_type,year,amount):
    """
    runs through all pages based on the parameters given (type,year)
    and returns a list the highest rated Media objects (only returns the amount specified when the function was called)
    """

    Media_list=list() #list of all objects (movies,shows or animated) that will be returned
    base_url='http://kinozal.tv/browse.php' #the base url that will be used to create a url for each new page

    url='http://kinozal.tv/browse.php?c=100'+str(media_type)+'%v=3&d='+str(year)#the url for the first page based on the search parameters provided
    while(True): #run an endless loop (the will stop once there are no additional pages to search)
        try:
            res=requests.get(url) #request the page
            res.raise_for_status() #raise exception in case of error
            page_soup=bs4.BeautifulSoup(res.text) #create a BeautifulSoup object

            objects_elm=page_soup.findAll("td",{"class":"nam"}) #find all the media objects on the page
            for i in objects_elm:
                print("next")
                try:
                    Media_list=Insert_Media(Handle_Object(i),Media_list) #for each piece of media create a Media object and insert into the existing list based on the rating and
                except AttributeError:
                    pass

            next_page_element=page_soup.find('a',rel="next")
            if next_page_element==None:
                break
            print('\n\n next page \n\n')
            print(len(Media_list))
            url=base_url+next_page_element['href']
        except requests.exceptions.ConnectionError:
            print('connection error, retrying...')
            time.sleep(5)

    for i in Media_list:
        print(i.get_rating())

if __name__ == '__main__':
    main(2,2018,1)
