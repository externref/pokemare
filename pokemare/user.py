class User(object):
    def __init__(self):
        self.identifier = 0
        self.name = ""
        self.starter_id = 0
        self.badges = []
        self.pokedollars = 0
        self.stars = 0

    def __copy__(self):
        user_copy = type(self)(self.identifier, self.name)
        user_copy.starter_id = self.starter_id
        user_copy.badges = self.badges
        user_copy.pokedollars = self.pokedollars
        user_copy.stars = self.stars
        return user_copy

    def load_from_data(self, data):
        self.identifier = data[1]
        self.name = data[2]
        self.starter_id = data[3]
