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
        except requests.exceptions.ConnectionError as exc:
            print exc
            print exc.errno #testing
            print 'shit'
            checkErr=re.compile(r'Errno (\d+)') #regex to find error code
            mo=checkErr.search(str(exc))
            if mo != None:
                print mo.group()
                if 'Errno 10060' == mo.group(): #retry connection because got no response
                    index-=1
                    logging.warning('no response from server(Errno 10060). Retrying...')
                elif 'Errno 10061' == mo.group(): #target machine activly refused
                    logging.warning('Target machine refused(Errno 10061). Retrying in 30 seconds')
                    time.sleep(30)
            else:
                logging.critical('Unknown error:',str(exc))
                quit()
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
    exception=''
    while (True):
        #download all movies page
        try:
            url='http://kinozal.tv/browse.php?c=100'+str(MSA)+'&v=1&d='+str(year)+'&t=4&page='+str(index)
            res=requests.get(url)
            res.raise_for_status()
            logging.debug('downloaded page')
            pageSoup=bs4.BeautifulSoup(res.text)
            logging.debug('created BeautifulSoup object')
            #get movies and add if movie is not already in list
            moviesElms=pageSoup.select('.nam')
            for i in range(len(moviesElms)):
                movie=handleMovie(moviesElms[i])
                logging.debug('got movie object')
                if movie not in movies:
                    movies=insertMovie(movies,movie)
                    logging.debug('inserted movie')
            #check if there is a next page



        except exception as exc:
            checkErr=re.compile(r'Errno (\d+)') #regex to find error code
            mo=checkErr.search(str(exc))
            if mo != None:
                print mo.group()
                if 'Errno 10060' == mo.group(0): #retry connection because got no response
                    logging.warning('no response from server(Errno 10060). Retrying...')

                elif 'Errno 10061' == mo.group(): #target machine activly refused
                    logging.warning('Target machine refused(Errno 10061). Retrying in 30 seconds')
                    time.sleep(30)

            else:
                logging.critical('Unknown error:',str(exc))
        nextPageElm=pageSoup.find('a',rel="next")

        if nextPageElm==None: #if no next page break loop
            break
        index+=1
    print str(len(movies))
    for i in range(numOfMovies):
        pass
        #print movies[i].getName()

    #return number of movies chosen
    logging.info('Movies returned')
    return movies[:numOfMovies]


if __name__=='__main__':
    getMovies('1','2005',10)
