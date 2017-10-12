#python 2.7
#moviesClass.py - containes the class Movie which is used by topMovies.py
class Movie:
    name=''
    rating=0
    votes=0
    def __init__(self,name,rating,votes):
        self.name=name
        self.rating=rating
        self.votes=votes
    def getName(self):
        return self.name
    def getRating(self):
        return self.rating
    def getVotes(self):
        return self.votes
    
