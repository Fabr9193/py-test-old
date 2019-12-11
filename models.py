import secrets

class User(object):
    def __init__(self, name, token=None, group_id=None):
        self.name = name
        self.token = self.create_token()
        self.group_id = group_id
    def create_token(self):
        return secrets.token_urlsafe()
        

class Group(object):
    def __init__(self, name):
        self.name = name



