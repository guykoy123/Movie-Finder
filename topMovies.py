#python 2.7
#topMovies.py - retrieves 15 top rated Movies/Shows/AnimatedMovies of a certain year from the site kinozal.tv

import bs4,requests, movieClass, time, re, random,logging


def handleMovie(movieElement):
    """Creates a Movie object from HTML element"""
    while True:
        try:
            #download movie page
            res=requests.get('http://kinozal.tv'+str(movieElement.find('a').get('href')))
            res.raise_for_status()
            break
        except requests.exceptions.ConnectionError as exc:
            logging.info('Connection Error, retrying in 30 seconds')
            time.sleep(30)

    soup=bs4.BeautifulSoup(res.text)
    #retrieve movie propeties from page
    #save movie name
    nameElm=soup.select('.content a')
    name=nameElm[0].getText()
    #get rating
    ratingElement=soup.find('span',itemprop="ratingValue")
    rating=float(ratingElement.getText())
    #get number of seeders
    votersElement=soup.find('span',itemprop='votes')
    votes=int(votersElement.getText())
    #create Movie object
    movie=movieClass.Movie(name,rating,votes)
    logging.debug('Movie object created')
    #return movie
    return movie


def insertMovie(movies,movie):
    if len(movies)==0:
        movies.append(movie)
    elif len(movies)==1:
        if movie.getRating()<movies[0].getRating():
            movies.append(movie)
        else:
            movies.insert(0,movie)
    else:
        low=len(movies)-1
        high=0
        while True: #run loop to insert new movie in the correct way by its rating
        #rewrite this part!!!!!!!!!!!!!!!
            middle=(low+high)/2

            if movies[middle].getRating()==movie.getRating():
                movies.insert(middle,movie)
                break
            elif low<=high:
                movies.append(movie)
                break
            else:
                if movies[middle].getRating()<movie.getRating():
                    low=middle-1
                    if low<0:
                        movies.insert(0,movie)
                    break
                else:
                    high=middle+1
                    if high>len(movies)-1:
                        movies.append(movie)
                        break
    logging.debug('movie added')
    print 'added movie'
    return movies


def setupLogging():
    logging.basicConfig(filename='getMoviesLog.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def getMovies(MSA,year,numOfMovies):
    setupLogging()
    movies=[]
    index=0
    while (True):
        #download all movies page
        while (True): #loop until page downloaded
            try:
                url='http://kinozal.tv/browse.php?c=100'+str(MSA)+'&v=1&d='+str(year)+'&t=4&page='+str(index)
                res=requests.get(url)
                res.raise_for_status()
                logging.debug('downloaded page')
                pageSoup=bs4.BeautifulSoup(res.text)
                logging.debug('created BeautifulSoup object')
                #get movies and add if movie is not already in list
                #mydivs = soup.findAll("div", { "class" : "stylelistrow" })
                moviesElms=pageSoup.findAll("td", { "class" : "nam" })
                print len(moviesElms)
                for i in moviesElms:
                    movie=handleMovie(i)
                    logging.debug('got movie object')
                    if movie not in movies:
                        movies=insertMovie(movies,movie)
                        logging.debug('inserted movie')
                        print 'inserted movie'
                break


            except requests.exceptions.ConnectionError as exc:
                logging.info('Connection Error, retrying in 30 seconds')
                time.sleep(30)
        #check if there is a next page
        nextPageElm=pageSoup.find('a',rel="next")
        if nextPageElm==None: #if no next page break loop
            break
        index+=1
    print str(len(movies))
    for i in range(min(numOfMovies,len(movies))):
        #pass
        print unicode(movies[i].getName())

    #return number of movies chosen
    logging.info('Movies returned')
    return movies[:min(numOfMovies,len(movies))]


if __name__=='__main__':
    getMovies('1','2005',10)
