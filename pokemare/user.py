class User(object):

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def __copy__(self):
        user_copy = type(self)(self.identifier, self.name)
        return user_copy
