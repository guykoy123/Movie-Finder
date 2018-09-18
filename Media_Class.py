class Media:
    name=''
    link=''
    rating=0
    votes=0

    def __init__(self,name,link,rating,votes):
        self.name=name
        self.link=link
        self.rating=rating
        self.votes=votes
    def get_name(self):
        return self.name

    def get_link(self):
        return self.link

    def get_rating(self):
        return self.rating

    def get_votes(self):
        return self.votes
